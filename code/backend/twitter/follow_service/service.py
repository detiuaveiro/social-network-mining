import gc
import logging
from typing import Dict, List

import keras.backend as keras_backend
import numpy as np

import messages_types
from credentials import TASK_FOLLOW_EXCHANGE, SERVICE_QUERY_EXCHANGE
from email_service.email import Email
from follow_service.utils import to_json, current_time, wait, convert_policies_to_model_input_data, get_labels, \
	update_tweets, get_full_text, update_models, get_all_tweets_per_policy
from rabbit_messaging import RabbitMessaging
import os
from follow_service.classifier import predict_soft_max, train_model
from follow_service.tweets_scrapper import get_data
from pymongo import MongoClient

logger = logging.getLogger("follow-service")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(open("follow_service.log", "w"))
handler.setFormatter(logging.Formatter(
	"[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s"))
logger.addHandler(handler)

WAIT_TIME_NO_TASKS = 10
THRESHOLD_FOLLOW_USER = 0.7
MEAN_WORDS_PER_TWEET = 120
NUMBER_TWEETS_PREDICT = 5

MONGO_URL = os.environ.get('MONGO_URL_SCRAPPER', 'localhost')
MONGO_PORT = 27017
MONGO_DB = os.environ.get('MONGO_DB_SCRAPPER', 'twitter_fu_service')


class Service(RabbitMessaging):
	def __init__(self, url, username, password, vhost, messaging_settings):
		super().__init__(url, username, password, vhost, messaging_settings)
		self.client = MongoClient(f"mongodb://{MONGO_URL}:{MONGO_PORT}/{MONGO_DB}")
		self.mongo_models = eval(f"self.client.{MONGO_DB}.models")
		self.mongo_policies_tweets = eval(f"self.client.{MONGO_DB}.policies_tweets")
		self.email_service = Email()

	def __send_message(self, data, message_type: messages_types.FollowServiceToServer):
		"""Function to send a new message to the server through rabbitMQ

		:param data: data to send
		:param message_type: type of message to send to server
		"""
		logger.debug(f"Sending message with type {messages_types.FollowServiceToServer(message_type).name}")
		self._send_message(to_json({
			'type': message_type,
			'timestamp': current_time(),
			'data': data
		}), SERVICE_QUERY_EXCHANGE)

	def __receive_message(self):
		"""Function to consume a new message from the follows's queue
		"""
		return self._receive_message(TASK_FOLLOW_EXCHANGE)

	def __setup(self):
		"""Function to setting up messaging queues and check if twitter credentials are ok
		"""
		logger.debug("Setting up messaging")
		self._setup_messaging()

		# send a request to get policies
		self.__send_message(data={}, message_type=messages_types.FollowServiceToServer.REQUEST_POLICIES)

	def __train_full_policy(self, not_trained_policies, model_input_data):

		policies_tweets = {}

		logger.debug(f"Training {not_trained_policies} policies")

		for policy_name in not_trained_policies:
			params = model_input_data[policy_name]
			tweets = []
			for q in params:
				tweets += get_full_text(get_data(q))

			policies_tweets[policy_name] = list(set(tweets))  # Ignoring repeated tweets

		update_tweets(self.mongo_policies_tweets, policies_tweets)

		new_models = train_model(self.mongo_policies_tweets, policies_tweets)

		args_per_label = dict([(label, model_input_data[label]) for label in not_trained_policies])
		update_models(self.mongo_models, new_models, args_per_label)

	def __train_new_policy_args(self, new_args_per_label, trained_labels):
		logger.debug(f"Updating arguments for a policy {new_args_per_label.keys()}")
		policies_tweets = {}
		new_args = {}
		for policy_name in new_args_per_label:
			tweets = []
			args, to_remove = new_args_per_label[policy_name]
			new_args[policy_name] = args
			for q in args:
				tweets += get_full_text(get_data(q))
			if not to_remove:  # Check this to to_Remove=True
				logger.debug("Adding new args")
				tweets += get_all_tweets_per_policy(self.mongo_policies_tweets, {'name': policy_name})[0]['tweets']
				for arg in trained_labels[policy_name]:
					new_args[policy_name].append(arg)
			else:
				logger.debug("Deleting new args")

			policies_tweets[policy_name] = list(set(tweets))

		update_tweets(self.mongo_policies_tweets, policies_tweets)
		new_models = train_model(self.mongo_policies_tweets, policies_tweets)

		update_models(self.mongo_models, new_models, new_args)

	def __train_models(self, policies: List[Dict], emails: List[str]):
		"""
		:param policies: dictionary in which each key is the name of the policy and the values are lists with the
			keywords of that policy
		"""
		logger.debug("Starting train process")
		model_input_data = convert_policies_to_model_input_data(policies)
		if len(model_input_data) < 2:
			logger.debug("Cant start training process. At least 2 policies need to be defined")
			return

		trained_labels = get_labels(self.mongo_models, list(model_input_data.keys()))

		new_args_per_label = {}
		for label in model_input_data:
			dif = ()
			if label not in trained_labels:
				continue
			if len(model_input_data[label]) < len(trained_labels[label]):
				dif = (model_input_data[label], True)
			elif len(model_input_data[label]) > len(trained_labels[label]):
				dif = (list(set(model_input_data[label]) - set(trained_labels[label])), False)

			if dif:
				new_args_per_label[label] = dif

		if len(trained_labels) == len(model_input_data) and not new_args_per_label:
			logger.debug("All policies have been already trained")
			return

		not_trained_policies = list(set(model_input_data.keys()) - set(trained_labels))

		if not_trained_policies or new_args_per_label:
			for email in emails:
				self.email_service.send_train_started(email)

		if not_trained_policies:
			self.__train_full_policy(not_trained_policies, model_input_data)

		if new_args_per_label:
			self.__train_new_policy_args(new_args_per_label, trained_labels)

		if not_trained_policies or new_args_per_label:
			for email in emails:
				self.email_service.send_train_finished(email)

		logger.debug(f"Training {not_trained_policies} policies process done")

		# Send a message to cc to change email status
		self.__send_message(data=None,
		                    message_type=messages_types.FollowServiceToServer.CHANGE_EMAIL_STATUS)


	def __predict_follow_user(self, user: Dict, tweets: List[str], policies, bot_id):
		"""
		:param user: user to predict if we want to follow or not
		:param tweets: list of tweets to give the ml model to predict
		"""

		tweets_to_use = sorted(tweets, key=lambda x: len(x), reverse=True)[:NUMBER_TWEETS_PREDICT]

		user_id = int(user['id_str'])
		heuristic = 0
		tweets_len_mean = np.mean([len(i) for i in tweets_to_use])

		if tweets_len_mean >= MEAN_WORDS_PER_TWEET or len(tweets_to_use) == 0:
			policies_labels = [p['name'] for p in policies]

			description = user['description']

			predictions = predict_soft_max(self.mongo_models, tweets_to_use + [description], policies_labels)

			keras_backend.clear_session()
			gc.collect()

			final_choices = {}

			for key in predictions:
				mean = np.mean(predictions[key])
				final_choices[key] = {
					'mean': mean,
					'length': len(predictions[key]),
					'final_score': mean * len(predictions[key])
				}

			best_choice = sorted(list(final_choices.items()), reverse=True, key=lambda c: c[-1]['final_score'])[0]
			picked_label, mean_score = best_choice[0], best_choice[-1]['mean']
			heuristic += mean_score

		status = bool(heuristic >= THRESHOLD_FOLLOW_USER)

		logger.debug(f"Request from bot with id <{bot_id}> to follow user with id: <{user_id}> "
		             f"<{'Accepted' if status else 'Denied'}> and heuristic of <{heuristic}>")

		self.__send_message(data={'user': user, 'status': status, 'bot_id_str': bot_id},
		                    message_type=messages_types.FollowServiceToServer.FOLLOW_USER)

	def __verify_if_new_policies(self, policies: List[Dict], emails: List[str]):
		"""
		:param policies: list of policies names to verify if we have models for them all
		"""
		self.__train_models(policies, emails)

	def run(self):
		"""Service's loop. As simple as a normal handler, tries to get tasks from the queue and, depending on the
			task, does a different action
		"""
		self.__setup()
		while True:
			try:
				logger.info(f"Getting next task from {TASK_FOLLOW_EXCHANGE}")
				task = self.__receive_message()

				if task:
					task_type, task_params = task['type'], task['params']
					logger.debug(
						f"Received task of type {messages_types.ServerToFollowService(task_type).name}")

					if task_type == messages_types.ServerToFollowService.POLICIES_KEYWORDS:
						self.__train_models(policies=task_params['data'], emails=[e['email'] for e in task_params['activated_notifications']])
					elif task_type == messages_types.ServerToFollowService.REQUEST_FOLLOW_USER:
						self.__predict_follow_user(user=task_params['user'], tweets=task_params['tweets'],
						                           policies=task_params['policies'], bot_id=task_params['bot_id_str'])
						self.__verify_if_new_policies(policies=task_params['all_policies'], emails=[e['email'] for e in task_params['activated_notifications']])
					else:
						logger.warning(f"Received unknown task type: {task_type}")
				else:
					logger.warning(
						f"There are not new messages on the tasks's queue. Waiting for <{WAIT_TIME_NO_TASKS} s>")

					wait(WAIT_TIME_NO_TASKS)
			except Exception as error:
				logger.exception(f"Error {error} on follow user service's loop: ")
