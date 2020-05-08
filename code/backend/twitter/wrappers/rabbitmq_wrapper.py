## @package twitter.wrappers
# coding: UTF-8
import functools
import pika
import time
import logging
import json

from pika.adapters.asyncio_connection import AsyncioConnection

from credentials import *

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
            heartbeat=10000,
            blocked_connection_timeout=10000
        )

        self.reconnection_attempt = 0
        self.MAX_RECONNECTIONS = 10
        self.connection = None
        self.channel = None

    def run(self):
        self.connection = AsyncioConnection(parameters=self.pika_parameters,
                                            on_open_callback=self._setup)
        self.connection.ioloop.run_forever()

    def _setup(self, _unused_connection):
        """
        Set up function, will start the connection, create all necessary exchanges and respective bindings from the
        parameters given from the constructor
        """

        self.connection.channel(on_open_callback=self.on_channel_open)

        # self.channel.basic_qos(prefetch_count=10, global_qos=True)
        # callback = functools.partial(self.on_queue_declareok, userdata=API_QUEUE)
        # print("ola1")
        # self.channel.queue_declare(queue=API_QUEUE, callback=callback)            # durable=True
        # print("ola2")

    def on_channel_open(self, channel):
        self.channel = channel

        # Declare Exchanges
        # log.info("Declaring exchanges")
        # self.channel.exchange_declare(
        #     exchange=TASKS_EXCHANGE,
        #     exchange_type='direct',
        #     durable=True
        # )

        callback = functools.partial(self.setup_queue, data={
            'exchange': DATA_EXCHANGE,
            'routing_key': DATA_ROUTING_KEY,
            'queue': API_QUEUE
        })
        self.channel.exchange_declare(
            exchange=DATA_EXCHANGE,
            durable=True,
            callback=callback
        )

        callback = functools.partial(self.setup_queue, data={
            'exchange': LOG_EXCHANGE,
            'routing_key': LOG_ROUTING_KEY,
            'queue': API_QUEUE
        })
        self.channel.exchange_declare(
            exchange=LOG_EXCHANGE,
            durable=True,
            callback=callback
        )

        callback = functools.partial(self.setup_queue, data={
            'exchange': QUERY_EXCHANGE,
            'routing_key': QUERY_ROUTING_KEY,
            'queue': API_QUEUE
        })
        self.channel.exchange_declare(
            exchange=QUERY_EXCHANGE,
            durable=True,
            callback=callback
        )

    def setup_queue(self, _unused_frame, data):
        callback = functools.partial(self.on_queue_declareok, data=data)
        self.channel.queue_declare(queue=data['queue'], durable=True, callback=callback)

    def on_queue_declareok(self, _unused_frame, data):

        callback = functools.partial(self.set_prefetch, queue_name=data['queue'])

        # Create Bindings
        log.info("Creating bindings")
        self.channel.queue_bind(
            queue=data['queue'],
            exchange=data['exchange'],
            routing_key=data['routing_key'],
            callback=callback
        )

        log.info("Connection to Rabbit Established")

    def set_prefetch(self, _unused_frame, queue_name):
        self.channel.basic_qos(prefetch_count=10, callback=functools.partial(self._receive, queue_name=queue_name))

    def _send(self, routing_key, message):
        """
        Routes the message to corresponding channel

        params:
        -------
        routing_key: (string) routing key to binding to queue
        message: (Dictionary) dictionary to be stringified and sent
        """

        self.channel.basic_publish(
            exchange="tasks_deliver",
            routing_key=routing_key,
            body=json.dumps(message)
        )

    def _receive(self, _unused_frame, queue_name):
        """
        Receives messages and puts them in the queue given from the argument

        params:
        -------
        queue_name : (string) Name of the queue to be declared
        """

        try:
            log.info(" [*] Waiting for Messages. To exit press CTRL+C")

            self.channel.basic_consume(queue=queue_name, on_message_callback=self.received_message_handler,
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
