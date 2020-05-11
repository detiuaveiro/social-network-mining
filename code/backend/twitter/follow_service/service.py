import gc
import logging
from typing import Dict, List

import keras.backend as keras_backend
import numpy as np

import messages_types
from credentials import TASK_FOLLOW_EXCHANGE, SERVICE_QUERY_EXCHANGE
from follow_service.utils import to_json, current_time, wait, convert_policies_to_model_input_data, get_labels, \
	update_tweets, get_full_text, update_models
from rabbit_messaging import RabbitMessaging
from wrappers.mongo_wrapper import MongoAPI
from follow_service.classifier import predict_soft_max, train_model
from follow_service.tweets_scrapper import get_data

logger = logging.getLogger("follow-service")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(open("follow_service.log", "w"))
handler.setFormatter(logging.Formatter(
	"[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s"))
logger.addHandler(handler)

WAIT_TIME_NO_TASKS = 10
THRESHOLD_FOLLOW_USER = 0.85
MEAN_WORDS_PER_TWEET = 80


class Service(RabbitMessaging):
	def __init__(self, url, username, password, vhost, messaging_settings):
		super().__init__(url, username, password, vhost, messaging_settings)
		self.mongo_client = MongoAPI()

	def __send_message(self, data, message_type: messages_types.FollowServiceToServer):
		"""Function to send a new message to the server through rabbitMQ

		:param data: data to send
		:param message_type: type of message to send to server
		"""

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

	def __train_models(self, policies: List[Dict]):
		"""
		:param policies: dictionary in which each key is the name of the policy and the values are lists with the
			keywords of that policy
		"""

		# Distinçao entre keywords e target???
		logger.debug("Starting train process")
		model_input_data = convert_policies_to_model_input_data(policies)
		if len(model_input_data) < 2:
			logger.debug("Cant start training process. At least 2 policies need to be defined")
			# Mandar uma mensagem para o Control Center ???
			return

		trained_labels = get_labels(self.mongo_client.models, list(model_input_data.keys()))

		if len(trained_labels) == len(model_input_data):
			logger.debug("All policies have been already trained")
			return

		not_trained_policies = list(set(model_input_data.keys()) - set(trained_labels))
		policies_tweets = {}

		logger.debug(f"Training {not_trained_policies} policies")

		for policy_name in not_trained_policies:
			params = model_input_data[policy_name]
			tweets = []
			for q in params:
				tweets += get_full_text(get_data(q))

			policies_tweets[policy_name] = list(set(tweets))  # Ignoring repeated tweets

		update_tweets(self.mongo_client.policies_tweets, policies_tweets)

		new_models = train_model(self.mongo_client.policies_tweets, policies_tweets)

		args_per_label = dict([(label, model_input_data[label]) for label in not_trained_policies])
		update_models(self.mongo_client.models, new_models, args_per_label)

		logger.debug(f"Training {not_trained_policies} policies process done")

	def __predict_follow_user(self, user: Dict, tweets: List[str], policies, bot_id):
		"""
		:param user: user to predict if we want to follow or not
		:param tweets: list of tweets to give the ml model to predict
		"""

		user_id = int(user['id_str'])
		heuristic = 0
		tweets_len_mean = np.mean([len(i) for i in tweets])

		if tweets_len_mean >= MEAN_WORDS_PER_TWEET or len(tweets) == 0:
			policies_labels = [p['name'] for p in policies]
			description = user['description']

			predictions = predict_soft_max(self.mongo_client.models, tweets + [description], policies_labels)

			keras_backend.clear_session()
			gc.collect()

			policies_confidence = {}

			for label in predictions:
				confidence, policy_name = label
				if policy_name not in policies_confidence:
					policies_confidence[policy_name] = []
				policies_confidence[policy_name].append(confidence)

			final_choices = {}

			for key in policies_confidence:
				mean = np.mean(
					policies_confidence[key] + [0 for _ in range(len(predictions) - len(policies_confidence[key]))])
				final_choices[key] = {
					'mean': mean,
					'length': len(policies_confidence[key]),
					'final_score': mean * len(policies_confidence[key]) if mean > 0 else
					len(policies_confidence[key])
				}

			best_choice = sorted(list(final_choices.items()), reverse=True, key=lambda c: c[-1]['final_score'])[0]
			picked_label, mean_score = best_choice[0], best_choice[-1]['mean']
			heuristic += mean_score

		status = bool(heuristic >= THRESHOLD_FOLLOW_USER)

		logger.debug(
			f"Request to follow user with id: {user_id} {'Accepted' if status else 'Denied'}")

		self.__send_message(data={'user': user, 'status': status, 'bot_id_str': bot_id},
		                    message_type=messages_types.FollowServiceToServer.FOLLOW_USER)

	def __verify_if_new_policies(self, policies: List[str]):
		"""
		:param policies: list of policies names to verify if we have models for them all
		"""
		# TODO -> verificar se temos modelos para todas as policies. se há alguma que não tenhamos, mandamos msg para o
		#  control center a pedir as keywords para as respetivas
		wait(10)

		if 1 == 1:  # to send the message requesting the respective policies
			self.__send_message(data={'policies': []},
			                    message_type=messages_types.FollowServiceToServer.REQUEST_POLICIES)

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
						f"Received task of type {messages_types.ServerToFollowService(task_type).name}: {task_params}")

					if task_type == messages_types.ServerToFollowService.POLICIES_KEYWORDS:
						self.__train_models(policies=task_params)
					elif task_type == messages_types.ServerToFollowService.REQUEST_FOLLOW_USER:
						self.__predict_follow_user(user=task_params['user'], tweets=task_params['tweets'],
						                           policies=task_params['policies'], bot_id=task_params['bot_id_str'])
					# self.__verify_if_new_policies(policies=task_params['policies'])
					else:
						logger.warning(f"Received unknown task type: {task_type}")
				else:
					logger.warning(
						f"There are not new messages on the tasks's queue. Waiting for <{WAIT_TIME_NO_TASKS} s>")

					wait(WAIT_TIME_NO_TASKS)
			except Exception as error:
				logger.exception(f"Error {error} on follow user service's loop: ")
