## @package twitter.wrappers
# coding: UTF-8
import functools
import json
import logging
import time

import pika
from pika.adapters.asyncio_connection import AsyncioConnection

from control_center.control_center import Control_Center
from credentials import RABBITMQ_URL, RABBITMQ_PORT, VHOST, RABBITMQ_USERNAME, RABBITMQ_PASSWORD, API_QUEUE, \
    API_FOLLOW_QUEUE, SERVICE_QUERY_EXCHANGE, SERVICE_QUERY_ROUTING_KEY, TASKS_QUEUE_PREFIX, TASKS_EXCHANGE, \
    TASK_FOLLOW_QUEUE, TASK_FOLLOW_EXCHANGE, DATA_EXCHANGE, DATA_ROUTING_KEY, LOG_ROUTING_KEY, LOG_EXCHANGE, \
    QUERY_EXCHANGE, QUERY_ROUTING_KEY

log = logging.getLogger('Rabbit')
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(open("rabbitmq.log", "w"))
handler.setFormatter(logging.Formatter("[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s"))
log.addHandler(handler)


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

        self._connection = None
        self.channels = {}

        self.exchanges_data = {API_QUEUE: [], API_FOLLOW_QUEUE: []}
        self.bots = []

        # consumer exchanges data
        self.exchanges_data[API_QUEUE].append({'exchange': DATA_EXCHANGE, 'routing_key': DATA_ROUTING_KEY,
                                               'publish_exchange': TASKS_EXCHANGE,
                                               'control_center': Control_Center(self)})
        self.exchanges_data[API_QUEUE].append({'exchange': LOG_EXCHANGE, 'routing_key': LOG_ROUTING_KEY,
                                               'publish_exchange': TASKS_EXCHANGE,
                                               'control_center': Control_Center(self)})
        self.exchanges_data[API_QUEUE].append({'exchange': QUERY_EXCHANGE, 'routing_key': QUERY_ROUTING_KEY,
                                               'publish_exchange': TASKS_EXCHANGE,
                                               'control_center': Control_Center(self)})

        self.exchanges_data[API_FOLLOW_QUEUE].append({'exchange': SERVICE_QUERY_EXCHANGE,
                                                      'routing_key': SERVICE_QUERY_ROUTING_KEY,
                                                      'publish_exchange': TASK_FOLLOW_EXCHANGE,
                                                      'control_center': Control_Center(self)})

        # publisher exchanges data
        self.publish_exchange = {
            TASKS_QUEUE_PREFIX: {'exchange': TASKS_EXCHANGE},
            TASK_FOLLOW_QUEUE: {'exchange': TASK_FOLLOW_EXCHANGE}
        }
        self.control_centers = {}

    def run(self):
        self.__connect()
        self._connection.ioloop.run_forever()

    def __connect(self):
        self._connection = AsyncioConnection(parameters=self.pika_parameters,
                                             on_open_callback=self.__setup,
                                             on_open_error_callback=self.__on_connection_open_error,
                                             on_close_callback=self.__on_connection_closed)
        log.info("Connected")

    def __setup(self, _unused_connection):
        """
        Set up function, will start the connection, create all necessary exchanges and respective bindings from the
        parameters given from the constructor
        """

        # consume queues
        self._connection.channel(on_open_callback=self.__on_api_channel_open)
        self._connection.channel(on_open_callback=self.__on_api_follow_channel_open)

        # publish queues
        # self._connection.channel(on_open_callback=self.__on_bot_tasks_channel_open)
        # self._connection.channel(on_open_callback=self.__on_follow_tasks_channel_open)

    def __on_api_channel_open(self, channel):
        self.__on_channel_open(channel=channel, queue=API_QUEUE)

    def __on_api_follow_channel_open(self, channel):
        self.__on_channel_open(channel=channel, queue=API_FOLLOW_QUEUE)

    def __on_bot_tasks_channel_open(self, channel):
        self.__on_tasks_channel_open(channel=channel, queue=TASKS_QUEUE_PREFIX)

    def __on_follow_tasks_channel_open(self, channel):
        self.__on_tasks_channel_open(channel=channel, queue=TASK_FOLLOW_QUEUE)

    def __on_tasks_channel_open(self, channel, queue):
        # self.channels[queue] = channel

        exchange = self.publish_exchange[queue]['exchange']

        log.info(f"Declaring exchange <{exchange}>")

        channel.exchange_declare(
            exchange=exchange,
            durable=True
        )

    def __on_channel_open(self, channel, queue):
        self.channels[queue] = channel

        log.info(f"Starting to configure channel <{channel}> with exchanges <{self.exchanges_data[queue]}>")

        for exchange_data in self.exchanges_data[queue]:
            exchange = exchange_data['exchange']
            routing_key = exchange_data['routing_key']

            log.info(f"Declaring exchange <{exchange}>")

            callback = functools.partial(self.__setup_queue, queue=queue, exchange=exchange, routing_key=routing_key,
                                         control_center=exchange_data['control_center'])
            self.channels[queue].exchange_declare(
                exchange=exchange,
                durable=True,
                callback=callback
            )

            # create the publish channel to each consumer channel
            self.control_centers[exchange] = self._connection.channel(
                on_open_callback=self.__on_bot_tasks_channel_open if exchange_data['publish_exchange'] == TASKS_EXCHANGE
                else self.__on_follow_tasks_channel_open)

    def __setup_queue(self, _unused_frame, queue, exchange, routing_key, control_center):
        callback = functools.partial(self.__on_queue_declared, queue=queue, exchange=exchange, routing_key=routing_key,
                                     control_center=control_center)
        self.channels[queue].queue_declare(queue=queue, durable=True, callback=callback)

    def __on_queue_declared(self, _unused_frame, queue, exchange, routing_key, control_center):

        callback = functools.partial(self.__set_prefetch, queue=queue, control_center=control_center)

        # Create Bindings
        log.info("Creating bindings")
        self.channels[queue].queue_bind(
            queue=queue,
            exchange=exchange,
            routing_key=routing_key,
            callback=callback
        )

        log.info("Connection to Rabbit Established")

    def __set_prefetch(self, _unused_frame, queue, control_center):
        self.channels[queue].basic_qos(
            prefetch_count=5, callback=functools.partial(self._receive, queue=queue, control_center=control_center))

    def __on_connection_open_error(self, _unused_connection, err):
        """This method is called by pika if the connection to RabbitMQ
        can't be established.
        Adapted from the example on https://github.com/pika/pika/blob/master/examples/asynchronous_consumer_example.py
        :param pika.SelectConnection _unused_connection: The connection
        :param Exception err: The error
        """
        log.error('Connection open failed: %s', err)
        self.__reconnect()

    def __on_connection_closed(self, _unused_connection, reason):
        """This method is invoked by pika when the connection to RabbitMQ is
        closed unexpectedly. Since it is unexpected, we will reconnect to
        RabbitMQ if it disconnects.
        Adapted from the example on https://github.com/pika/pika/blob/master/examples/asynchronous_consumer_example.py
        :param Exception reason: exception representing reason for loss of
            connection.
        """
        log.warning('Connection closed, reconnect necessary: %s', reason)
        self.__reconnect()

    def __reconnect(self):
        """Will be invoked if the connection can't be opened or is
        closed. Indicates that a reconnect is necessary then stops the
        ioloop.
        Adapted from the example on https://github.com/pika/pika/blob/master/examples/asynchronous_consumer_example.py
        """
        self.stop_and_restart()

    def stop_and_restart(self):
        log.info('Stopping')
        self.__stop_consuming()
        log.info('Stopped')
        time.sleep(5*len(self.channels.values()))
        self.__connect()

    def __stop_consuming(self):
        """Tell RabbitMQ that you would like to stop consuming by sending the
        Basic.Cancel RPC command.
        Adapted from the example on https://github.com/pika/pika/blob/master/examples/asynchronous_consumer_example.py
        """
        log.info('Sending a Basic.Cancel RPC command to RabbitMQ')
        for channel in self.channels.values():
            try:
                callback = functools.partial(self.__close_channel, channel=channel)
                channel.basic_cancel(callback=callback)
                log.debug(f"Stopped channel {channel}")
            except Exception as error:
                log.exception(f"Could not cancel the channel because of error <{error}>")

    @staticmethod
    def __close_channel(_unused_frame, channel):
        """Call to close the channel with RabbitMQ cleanly by issuing the
        Channel.Close RPC command.
        """
        log.info('Closing the channel')
        channel.close()

    def send(self, queue, routing_key, message, father_exchange):
        """
        Routes the message to corresponding channel

        params:
        -------
        routing_key: (string) routing key to binding to queue
        message: (Dictionary) dictionary to be stringified and sent
        """

        # self.channels[queue]
        exchange = self.publish_exchange[queue]['exchange']

        log.info(f"Sending message to channel number <{self.control_centers[father_exchange].channel_number}> "
                 f"from exchange <{father_exchange}>")
        self.control_centers[father_exchange].basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=json.dumps(message)
        )

    def _receive(self, _unused_frame, queue, control_center):
        """
        Receives messages and puts them in the queue given from the argument

        params:
        -------
        queue_name : (string) Name of the queue to be declared
        """

        log.info(" [*] Waiting for Messages. To exit press CTRL+C")

        self.channels[queue].basic_consume(queue=queue, on_message_callback=control_center.received_message_handler)

    def _received_message_handler(self, channel, method, properties, body):
        """Function to rewrite on the class that inherits this class
        """
        pass

    def _close(self):
        """
        Close the connection with the Rabbit MQ server
        """
        log.info("Closing connection")
        self._connection.ioloop.stop()
        self._connection.close()
        
    def close(self):
        for queue in self.exchanges_data:
            for exchange_data in self.exchanges_data[queue]:
                control_center = exchange_data['control_center']
                control_center.close()

        self._close()
