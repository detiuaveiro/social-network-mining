import logging
from typing import Dict, List

import messages_types
from credentials import TASK_FOLLOW_EXCHANGE, SERVICE_QUERY_EXCHANGE
from follow_service.utils import to_json, current_time, wait
from rabbit_messaging import RabbitMessaging

logger = logging.getLogger("follow-service")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(open("follow_service.log", "w"))
handler.setFormatter(logging.Formatter(
	"[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s"))
logger.addHandler(handler)


WAIT_TIME_NO_TASKS = 2


class Service(RabbitMessaging):
	def __init__(self, url, username, password, vhost, messaging_settings):
		super().__init__(url, username, password, vhost, messaging_settings)

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
		wait(10)

	def __predict_follow_user(self, user_id: str, tweets: List[str]):
		"""

		:param user: user_id to predict if we want to follow or not
		:param tweets: list of tweets to give the ml model to predict
		"""

	def run(self):
		"""Service's loop. As simple as a normal handler, tries to get tasks from the queue and, depending on the
			task, does a different action
		"""
		self.__setup()

		try:
			logger.info(f"Getting next task from {TASK_FOLLOW_EXCHANGE}")
			task = self.__receive_message()

			if task:
				task_type, task_params = task['type'], task['params']
				logger.debug(f"Received task of type {messages_types.ServerToFollowService(task_type).name}: {task_params}")

				if task_type == messages_types.ServerToFollowService.POLICIES_KEYWORDS:
					self.__train_models(policies=task_params)
				elif task_type == messages_types.ServerToFollowService.REQUEST_FOLLOW_USER:
					self.__predict_follow_user(user_id=task_params['user'], tweets=task_params['tweets'])
				else:
					logger.warning(f"Received unknown task type: {task_type}")
			else:
				logger.warning(f"There are not new messages on the tasks's queue. Waiting for <{WAIT_TIME_NO_TASKS} s>")

				wait(WAIT_TIME_NO_TASKS)
		except Exception as error:
			logger.exception(f"Error {error} on bot's loop: ")
