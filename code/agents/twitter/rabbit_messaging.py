import logging
from typing import Dict
from pyrabbit2.http import NetworkError
from pyrabbit2.api import Client

from utils import current_time

logger = logging.getLogger("rabbit-messaging")
logger.setLevel(logging.DEBUG)


class MessagingSettings:
	def __init__(self, exchange, queue=None, routing_key=None):
		self.exchange = exchange
		self.queue = queue
		self.routing_key = routing_key

	def __str__(self) -> str:
		return f"exchange={self.exchange}, queue={self.queue}, routing_key={self.routing_key}"


class RabbitMessaging:
	def __init__(self, url, username, password, vhost, settings: Dict[str, MessagingSettings], reconnect_max_iterations=5):
		self.__url = url
		self.__username = username
		self.__password = password

		#
		self.vhost = vhost
		self.settings = settings

		self._messaging: Client

		self.__reconnect_max_iterations = reconnect_max_iterations

		# first connection
		self.__connect()

	def __reconnect_messaging(function):
		"""Decorator to try to reconnect multiple times if the connection to RabbitMQ fails

		:param function: function to decorate
		"""
		def wrapper(self, *args, **kwargs):
			for current_reconnect in range(self.__reconnect_max_iterations):
				try:
					return function(self, *args, **kwargs)
				except NetworkError as error:
					logger.error(f"{current_time()}: Connection to RabbitMQ lost. Trying to reconnect...")
					self.__connect()

					if current_reconnect == self.__reconnect_max_iterations - 1:
						raise error
		return wrapper

	@__reconnect_messaging
	def __setup_messaging(self):
		"""Private method for setting up the messaging connections
		"""
		for current_setting_name in self.settings:
			current_setting = self.settings[current_setting_name]

			logger.info(f"Setting up Messaging to: {current_setting}\n"
						 f"Connecting to exchange {current_setting.exchange}")
			self.messaging.create_exchange(vhost=self.vhost, name=current_setting.exchange, xtype="direct")

			if current_setting.queue and current_setting.routing_key:
				logger.info(f"Creating queue {current_setting.queue}")
				self.messaging.create_queue(vhost=self.vhost, name=current_setting.queue, durable=True)

				logger.info(f"Binding exchange to queue {current_setting.queue} with key {current_setting.routing_key}")
				self.messaging.create_binding(vhost=self.vhost, exchange=current_setting.exchange,
											  queue=current_setting.queue, rt_key=current_setting.routing_key)

			logger.info(f"Connected to Messaging Service using: {current_setting.__str__()}")
			logger.info("---------------------------------------")

	def __connect(self):
		self.messaging = Client(api_url=self.__url, user=self.__username, passwd=self.__password)

	def run(self):
		self.__setup_messaging()
