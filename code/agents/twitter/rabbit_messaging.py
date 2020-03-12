import logging
from pyrabbit2.http import NetworkError
from pyrabbit2.api import Client

from utils import current_time

logger = logging.getLogger("rabbit-messaging")
logger.setLevel(logging.DEBUG)


class RabbitMessaging:
	def __init__(self, url, username, password, reconnect_max_iterations=5):
		self.__url = url
		self.__username = username
		self.__password = password

		self._messaging: Client

		self.__reconnect_max_iterations = reconnect_max_iterations

		# first connection
		self.__connect()

	def __reconnect_messaging(function):
		"""Decorator to try to reconnect multiple times if the connection to RabbitMQ fails

		:param function: function to decorate
		"""
		def wrapper(self, *args, **kwargs):
			for current_reconnect in range(self.reconnect_max_iterations):
				try:
					return function(self, *args, **kwargs)
				except NetworkError as error:
					logger.error(f"{current_time()}: Connection to RabbitMQ lost. Trying to reconnect...")
					self.__connect()

					if current_reconnect == self.reconnect_max_iterations - 1:
						raise error
		return wrapper

	@__reconnect_messaging
	def __setup_messaging(self):
		"""
			Private method for setuping the messaging connections
		"""
		print("ola")
		# logger.debug("Setting up Messaging to: Receive Tasks")
		# logger.debug(f"Connecting to exchange {self.tasks_exchange}")
		# self.messaging.create_exchange(vhost=self.vhost, name=self.tasks_exchange, xtype="direct")
		# logger.debug(f"Creating queue {self.tasks_queue}")
		# self.messaging.create_queue(vhost=self.vhost, name=self.tasks_queue, durable=True)
		# logger.debug(f"Binding exchange to queue {self.tasks_queue} with key {self.tasks_routing_key}")
		# self.messaging.create_binding(vhost=self.vhost, exchange=self.tasks_exchange,
		# 							  queue=self.tasks_queue, rt_key=self.tasks_routing_key)
		# logger.info("---------------------------------------")
		# logger.info(
		# 	f"Connected to Messaging Service using: exchange={self.tasks_exchange}, queue={self.tasks_queue}, routing_key={self.tasks_routing_key}")
		# logger.info("Ready to receive tasks")
#
		# logger.debug("---------------------------------------")
		# logger.debug("Setting up Messaging to: Upload Logs")
		# logger.debug(f"Connecting to exchange {self.logger_exchange}")
		# self.messaging.create_exchange(vhost=self.vhost, name=self.logger_exchange, xtype="direct")
		# logger.info("---------------------------------------")
		# logger.info(
		# 	f"Connected to Messaging Service using: exchange={self.logger_exchange}")
		# logger.info("Ready to: Upload Logs")
#
		# logger.debug("---------------------------------------")
		# logger.debug("Setting up Messaging to: Make Queries")
		# logger.debug(f"Connecting to exchange {self.query_exchange}")
		# self.messaging.create_exchange(vhost=self.vhost, name=self.query_exchange, xtype="direct")
		# logger.info("---------------------------------------")
		# logger.info(
		# 	f"Connected to Messaging Service using: exchange={self.query_exchange}")
		# logger.info("Ready to: Make Queries")
#
		# logger.debug("---------------------------------------")
		# logger.debug("Setting up Messaging to: Upload Data")
		# logger.debug(f"Connecting to exchange {self.data_exchange}")
		# self.messaging.create_exchange(vhost=self.vhost, name=self.data_exchange, xtype="direct")
		# logger.info("---------------------------------------")
		# logger.info(
		# 	f"Connected to Messaging Service using: exchange={self.data_exchange}")
		# logger.info("Ready to: Upload Data")

	def __connect(self):
		self.messaging = Client(api_url=self.url, user=self.username, passwd=self.password)

	def run(self):
		self.__setup_messaging()
