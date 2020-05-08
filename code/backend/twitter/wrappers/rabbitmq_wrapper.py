## @package twitter.wrappers
# coding: UTF-8
import functools
import pika
import time
import logging
import json

from pika.adapters.asyncio_connection import AsyncioConnection

from credentials import RABBITMQ_URL, RABBITMQ_PORT, VHOST, RABBITMQ_USERNAME, RABBITMQ_PASSWORD, API_QUEUE, \
    API_FOLLOW_QUEUE, DATA_EXCHANGE, DATA_ROUTING_KEY, LOG_ROUTING_KEY, LOG_EXCHANGE, QUERY_EXCHANGE, \
    QUERY_ROUTING_KEY, SERVICE_QUERY_EXCHANGE, SERVICE_QUERY_ROUTING_KEY, TASKS_QUEUE_PREFIX, TASKS_EXCHANGE, \
    TASK_FOLLOW_QUEUE, TASK_FOLLOW_EXCHANGE

log = logging.getLogger('Rabbit')
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(open("rabbitmq.log", "w"))
handler.setFormatter(logging.Formatter("[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s"))
log.addHandler(handler)

WAIT_TIME = 1


class Rabbitmq:
    """Class representing Rabbit MQ"""

    def __init__(self, host=RABBITMQ_URL, port=RABBITMQ_PORT, vhost=VHOST, username=RABBITMQ_USERNAME,
                 password=RABBITMQ_PASSWORD):
        """
        Create a Rabbit MQ instance which represents a connection to a Rabbit MQ server

        Parameters
        ----------
        host : str
            Hostname
        port : int
            Port Number
        vhost : str
            Virtual host used to avoid conflicts between instances
        username : str
            Username for authentication
        password : str
            Password for authentication
        """

        # Setting up pika credentials and parameters
        pika_credentials = pika.PlainCredentials(username, password)

        self.pika_parameters = pika.ConnectionParameters(
            host=host,
            port=port,
            virtual_host=vhost,
            credentials=pika_credentials,
            heartbeat=600,
            blocked_connection_timeout=300
        )

        self.connection = None
        self.channels = {}

        self.exchange = {API_QUEUE: [], API_FOLLOW_QUEUE: []}

        # consumer exchanges data
        self.exchange[API_QUEUE].append({'exchange': DATA_EXCHANGE, 'routing_key': DATA_ROUTING_KEY})
        self.exchange[API_QUEUE].append({'exchange': LOG_EXCHANGE, 'routing_key': LOG_ROUTING_KEY})
        self.exchange[API_QUEUE].append({'exchange': QUERY_EXCHANGE, 'routing_key': QUERY_ROUTING_KEY})
        self.exchange[API_FOLLOW_QUEUE].append({'exchange': SERVICE_QUERY_EXCHANGE,
                                                'routing_key': SERVICE_QUERY_ROUTING_KEY})

        # publisher exchanges data
        self.publish_exchange = {TASKS_QUEUE_PREFIX: {'exchange': TASKS_EXCHANGE}}
        self.publish_exchange = {TASK_FOLLOW_QUEUE: {'exchange': TASK_FOLLOW_EXCHANGE}}

    def run(self):
        self.connection = AsyncioConnection(parameters=self.pika_parameters,
                                            on_open_callback=self.__setup)
        self.connection.ioloop.run_forever()

    def __setup(self, _unused_connection):
        """
        Set up function, will start the connection, create all necessary exchanges and respective bindings from the
        parameters given from the constructor
        """

        # consume queues
        self.connection.channel(on_open_callback=self.__on_api_channel_open)
        self.connection.channel(on_open_callback=self.__on_api_follow_channel_open)

        # publish queues
        self.connection.channel(on_open_callback=self.__on_bot_tasks_channel_open)

    def __on_api_channel_open(self, channel):
        self.__on_channel_open(channel=channel, queue=API_QUEUE)

    def __on_api_follow_channel_open(self, channel):
        self.__on_channel_open(channel=channel, queue=API_FOLLOW_QUEUE)

    def __on_bot_tasks_channel_open(self, channel):
        self.__on_tasks_channel_open(channel=channel, queue=TASKS_QUEUE_PREFIX)

    def __on_tasks_channel_open(self, channel, queue):
        self.channels[queue] = channel

        exchange = self.publish_exchange[queue]['exchange']

        log.info(f"Declaring exchange <{exchange}>")

        self.channels[queue].exchange_declare(
            exchange=exchange,
            durable=True
        )

    def __on_channel_open(self, channel, queue):
        self.channels[queue] = channel

        for exchange_data in self.exchange[queue]:
            log.info(f"Declaring exchange <{exchange_data['exchange']}>")

            callback = functools.partial(self.__setup_queue, queue=queue, **exchange_data)
            self.channels[queue].exchange_declare(
                exchange=exchange_data['exchange'],
                durable=True,
                callback=callback
            )

    def __setup_queue(self, _unused_frame, queue, exchange, routing_key):
        callback = functools.partial(self.__on_queue_declared, queue=queue, exchange=exchange, routing_key=routing_key)
        self.channels[queue].queue_declare(queue=queue, durable=True, callback=callback)

    def __on_queue_declared(self, _unused_frame, queue, exchange, routing_key):

        callback = functools.partial(self.__set_prefetch, queue=queue)

        # Create Bindings
        log.info("Creating bindings")
        self.channels[queue].queue_bind(
            queue=queue,
            exchange=exchange,
            routing_key=routing_key,
            callback=callback
        )

        log.info("Connection to Rabbit Established")

    def __set_prefetch(self, _unused_frame, queue):
        self.channels[queue].basic_qos(prefetch_count=10, callback=functools.partial(self._receive, queue=queue))

    def _send(self, queue, routing_key, message):
        """
        Routes the message to corresponding channel

        params:
        -------
        routing_key: (string) routing key to binding to queue
        message: (Dictionary) dictionary to be stringified and sent
        """

        self.channels[queue].basic_publish(
            exchange=self.publish_exchange[queue]['exchange'],
            routing_key=routing_key,
            body=json.dumps(message)
        )

    def _receive(self, _unused_frame, queue):
        """
        Receives messages and puts them in the queue given from the argument

        params:
        -------
        queue_name : (string) Name of the queue to be declared
        """

        try:
            log.info(" [*] Waiting for Messages. To exit press CTRL+C")

            self.channels[queue].basic_consume(queue=queue, on_message_callback=self.received_message_handler,
                                               auto_ack=True)
            # self.channel.start_consuming()
        except Exception as e:
            log.exception(f"Exception <{e}> detected:")
            log.warning("Attempting reconnection after waiting time...")
            time.sleep(WAIT_TIME)
            # self.connect()
            log.debug("Setup completed")
            # self._receive(queue_name)

    def received_message_handler(self, channel, method, properties, body):
        """Function to rewrite on the class that inherits this class
        """
        pass

    def _close(self):
        """
        Close the connection with the Rabbit MQ server
        """
        log.info("Closing connection")
        self.connection.ioloop.stop()
        self.connection.close()
