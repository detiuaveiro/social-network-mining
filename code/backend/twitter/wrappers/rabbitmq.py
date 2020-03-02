import pika
import json
import logging
import sys
import time
from dbwriter import DBWriter
sys.path.append('..')
from credentials import *

log = logging.getLogger('Rabbit')
log.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s"))
log.addHandler(handler)

WAIT_TIME = 10

class Rabbitmq():
    """Class representing Rabbit MQ"""

    def __init__(self, host=RABBITMQ_URL, port=RABBITMQ_PORT, vhost=RABBITMQ_VHOST, username=RABBITMQ_USERNAME, password=RABBITMQ_PASSWORD):
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

        ## Setting up pika credentials and parameters
        pika_credentials = pika.PlainCredentials(username, password)
        self.pika_parameters = pika.ConnectionParameters(host=host,
                                                        port=port,
                                                        virtual_host=vhost,
                                                        credentials=pika_credentials,
                                                        heartbeat=600,
                                                        blocked_connection_timeout=300)

        self.reconnection_attempt = 0
        self.MAX_RECONNECTIONS = 10
        self.connection = None
        self.channel = None
    
    def _setup(self):
        """
        Set up function, will start the connection, create all necessary exchanges and respective bindings from the parameters given from the constructor
        """
    
        self.connection = pika.BlockingConnection(self.pika_parameters)

        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='API', durable=True)

        #Declare Exchanges
        log.info("Declaring exchanges")
        self.channel.exchange_declare(exchange='task_deliver',
                                    exchange_type='direct',
                                    durable=True)

        self.channel.exchange_declare(exchange='twitter_data',
                                    exchange_type='direct',
                                    durable=True)

        self.channel.exchange_declare(exchange='logs',
                                    exchange_type='direct',
                                    durable=True)

        self.channel.exchange_declare(exchange='queries',
                                    exchange_type='direct',
                                    durable=True)

        #Create Bindings
        log.info("Creating bindings")
        self.channel.queue_bind(exchange='data',
                                queue="API",
                                routing_key="data.twitter")
        
        self.channel.queue_bind(exchange="twitter_data",
                                queue="API",
                                routing_key='data.twitter')

        self.channel.queue_bind(exchange="logs",
                                queue="API",
                                routing_key='logs.twitter')

        self.channel.queue_bind(exchange="queries",
                                queue="API",
                                routing_key='queries.twitter')
        
        ## Implement a task manager
        self.database_writer = DBWriter()

        log.info("Connection to Rabbit Established")

    def send(self, routing_key, message):
        """ 
        Routes the message to corresponding channel

        params:
        -------
        routing_key: (string) routing key to bding to queue
        message: (Dictionary) dictionary to be stringified and sent
        """

        self.channel.basic_publish(exchange="tasks_deliver",
                                    routing_key=routing_key,
                                    body=json.dumps(message)
                                    )

    def receive(self, queue_name='API'):
        """
        Receives messages and puts thme in the queue given from the argument

        params:
        -------
        queue_name : (string) Name of the queue to be declared
        """

        try:
            self.channel.queue_declare(queue=queue_name,
                                    durable=True)
            
            log.info(" [*] Waiting for Messages. To exit press CTRL+C")
            
            def callback(channel, method, properties, body):
                log.info("MESSAGE RECEIVED")            
                message = json.loads(body)
                self.database_writer.menu(message['type'], message)

            self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
            self.channel.start_consuming()

        except Exception as e:
            log.warning("Exception detected: {0}".format(e))
            log.warning("Attempting reconnection after waiting time...")
            time.sleep(WAIT_TIME)
            self._setup()
            log.debug("Setup completed")
            self.receive(queue_name)
    
    def close(self):
        """
        Close the connection with the Rabbit MQ server
        """
        self.connection.close()

if __name__ == "__main__":
    rabbit = Rabbitmq()
    rabbit._setup()
    rabbit.receive()
    rabbit.close()
