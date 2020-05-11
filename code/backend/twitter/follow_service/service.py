import logging
from typing import Dict, List

import messages_types
from credentials import TASK_FOLLOW_EXCHANGE, SERVICE_QUERY_EXCHANGE, MONGO_FULL_URL
from follow_service.utils import to_json, current_time, wait
from rabbit_messaging import RabbitMessaging
from wrappers.mongo_wrapper import MongoAPI
from follow_service.classifier import predict_soft_max
import numpy as np
import gc
import keras.backend as keras_backend

logger = logging.getLogger("follow-service")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(open("follow_service.log", "w"))
handler.setFormatter(logging.Formatter(
	"[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s"))
logger.addHandler(handler)

WAIT_TIME_NO_TASKS = 2
THRESHOLD_FOLLOW_USER = 0.8
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

	def __train_models(self, policies: Dict[str, List[str]]):
		"""
		:param policies: dictionary in which each key is the name of the policy and the values are lists with the
			keywords of that policy
		"""
		# TODO -> verificar aqui se já existe o modelo para uma dada policie recebida, treinar e guardar no mongo.
		#  se o modelo já existe, não fazer nada e fazer logo return

		print(policies)
		wait(10)

		if 1 == 1:  # send the tweets we have collected with this method
			self.__send_message(data={'tweets': []},
			                    message_type=messages_types.FollowServiceToServer.SAVE_TWEETS)

	def __predict_follow_user(self, user_id: str, tweets: List[str], policies, description: str):
		"""
		:param user_id: user_id to predict if we want to follow or not
		:param tweets: list of tweets to give the ml model to predict
		"""

		heuristic = 0
		tweets_len_mean = np.mean([len(i) for i in tweets])

		if tweets_len_mean >= MEAN_WORDS_PER_TWEET or len(tweets) == 0:
			policies_labels = [p['name'] for p in policies]

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

		logger.debug(
			f"Request to follow user with id: {user_id} {'Accepted' if heuristic >= THRESHOLD_FOLLOW_USER else 'Denied'}")

		if heuristic >= THRESHOLD_FOLLOW_USER:  # to follow the user
			self.__send_message(data={'user': user_id}, message_type=messages_types.FollowServiceToServer.FOLLOW_USER)

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
						self.__predict_follow_user(user_id=task_params['user'], tweets=task_params['tweets'],
						                           policies=task_params['policies'],
						                           description=task_params['description'])
					# self.__verify_if_new_policies(policies=task_params['policies'])
					else:
						logger.warning(f"Received unknown task type: {task_type}")
				else:
					logger.warning(
						f"There are not new messages on the tasks's queue. Waiting for <{WAIT_TIME_NO_TASKS} s>")

					wait(WAIT_TIME_NO_TASKS)
			except Exception as error:
				logger.exception(f"Error {error} on follow user service's loop: ")
