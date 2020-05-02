## @package twitter.wrappers
# coding: UTF-8

import pika
import time
import logging
import json

from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection

from credentials import *

log = logging.getLogger('Rabbit')
log.setLevel(logging.INFO)
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
            heartbeat=1000,
            blocked_connection_timeout=1000
        )

        self.reconnection_attempt = 0
        self.MAX_RECONNECTIONS = 10
        self.connection = None
        self.channel = None
        self._setup()
    
    def _setup(self):
        """
        Set up function, will start the connection, create all necessary exchanges and respective bindings from the
        parameters given from the constructor
        """
    
        self.connection: BlockingConnection = pika.BlockingConnection(self.pika_parameters)

        self.channel: BlockingChannel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=500, global_qos=True)
        self.channel.queue_declare(queue=API_QUEUE, durable=True)

        # Declare Exchanges
        log.info("Declaring exchanges")
        self.channel.exchange_declare(
            exchange=TASKS_EXCHANGE,
            exchange_type='direct',
            durable=True
        )

        self.channel.exchange_declare(
            exchange=DATA_EXCHANGE,
            exchange_type='direct',
            durable=True
        )

        self.channel.exchange_declare(
            exchange=LOG_EXCHANGE,
            exchange_type='direct',
            durable=True
        )

        self.channel.exchange_declare(
            exchange=QUERY_EXCHANGE,
            exchange_type='direct',
            durable=True
        )

        # Create Bindings
        log.info("Creating bindings")
        self.channel.queue_bind(
            exchange=DATA_EXCHANGE,
            queue=API_QUEUE,
            routing_key=DATA_ROUTING_KEY
        )

        self.channel.queue_bind(
            exchange=LOG_EXCHANGE,
            queue=API_QUEUE,
            routing_key=LOG_ROUTING_KEY
        )

        self.channel.queue_bind(
            exchange=QUERY_EXCHANGE,
            queue=API_QUEUE,
            routing_key=QUERY_ROUTING_KEY
        )
        
        log.info("Connection to Rabbit Established")

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

    def _receive(self, queue_name='API'):
        """
        Receives messages and puts them in the queue given from the argument

        params:
        -------
        queue_name : (string) Name of the queue to be declared
        """

        try:
            self.channel.queue_declare(
                queue=queue_name,
                durable=True
            )
            
            log.info(" [*] Waiting for Messages. To exit press CTRL+C")

            self.channel.basic_consume(queue=queue_name, on_message_callback=self.received_message_handler,
                                       auto_ack=True)
            self.channel.start_consuming()
        except Exception as e:
            log.exception(f"Exception <{e}> detected:")
            log.warning("Attempting reconnection after waiting time...")
            time.sleep(WAIT_TIME)
            self._setup()
            log.debug("Setup completed")
            self._receive(queue_name)

    def received_message_handler(self, channel, method, properties, body):
        """Function to rewrite on the class that inherits this class
        """
        pass

    def _close(self):
        """
        Close the connection with the Rabbit MQ server
        """
        self.connection.close()
