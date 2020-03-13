import logging
import json
from typing import Dict, List
from pyrabbit2.http import NetworkError
from pyrabbit2.api import Client

from utils import current_time, from_json

logger = logging.getLogger("rabbit-messaging")
logger.setLevel(logging.DEBUG)


class MessagingSettings:
	def __init__(self, exchange, routing_key, queue=None):
		self.exchange = exchange
		self.routing_key = routing_key
		self.queue = queue

	def __str__(self) -> str:
		return f"exchange={self.exchange}, routing_key={self.routing_key}, queue={self.queue}"


class RabbitMessaging:
	def __init__(self, url, username, password, vhost, settings: Dict[str, MessagingSettings], reconnect_max_iterations=5):
		self.__url = url
		self.__username = username
		self.__password = password

		#
		self.vhost = vhost
		self.settings = settings

		self.__messaging: Client = None

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
					logger.error(f"{current_time(str_time=True)}: Connection to RabbitMQ lost. Trying to reconnect...")
					self.__connect()

					if current_reconnect == self.__reconnect_max_iterations - 1:
						raise error
		return wrapper

	def __connect(self):
		self.messaging = Client(api_url=self.__url, user=self.__username, passwd=self.__password)

	@__reconnect_messaging
	def __setup_messaging(self):
		"""Private method for setting up the messaging connections
		"""
		
		for current_setting_name in self.settings:
			current_setting = self.settings[current_setting_name]
			
			logger.info(f"Setting up Messaging to: {current_setting}\n"
						 f"Connecting to exchange {current_setting.exchange}")
			self.messaging.create_exchange(vhost=self.vhost, name=current_setting.exchange, xtype="direct")

			if current_setting.queue:
				logger.info(f"Creating queue {current_setting.queue}")
				self.messaging.create_queue(vhost=self.vhost, name=current_setting.queue, durable=True)

				logger.info(f"Binding exchange to queue {current_setting.queue} with key {current_setting.routing_key}")
				self.messaging.create_binding(vhost=self.vhost, exchange=current_setting.exchange,
											  queue=current_setting.queue, rt_key=current_setting.routing_key)

			logger.info(f"Connected to Messaging Service using: {current_setting.__str__()}")
			logger.info("---------------------------------------")

	@__reconnect_messaging
	def _send_message(self, data: json, send_to: str):
		"""Function to publish a message on one of the rabbitMQ's exchanges

		:param data: data to publish in json format
		:param send_to: where to publish the data; corresponds to a str key in self.settings, where that key maps to
			an object with the exchange and routing key values
		"""

		send_to = self.settings[send_to]
		logger.debug(f"Sending message <{data}> to exchange <{send_to.exchange}> with routing_key <{send_to.routing_key}>")
		self.__messaging.publish(vhost=self.vhost, xname=send_to.exchange, rt_key=send_to.routing_key, payload=data)

	def _receive_message(self, receive_from: str) -> Dict:
		"""Function to get a message from a specific rabbitMQ exchange
			:param receive_from: where to get the data; corresponds to a str key in self.settings, where that key
				maps to an object with the exchange and routing key values
		"""

		receive_from = self.settings[receive_from]
		msg: List[Dict] = self.__messaging.get_messages(vhost=self.vhost, qname=receive_from.queue, count=1)

		if msg and msg[0].get("payload", None):
			return from_json(msg[0]["payload"])
		return {}

	def _run(self):
		self.__setup_messaging()
