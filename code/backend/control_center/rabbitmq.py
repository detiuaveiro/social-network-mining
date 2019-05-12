import pika
import json
import time
from task import Task

class Rabbitmq():
    def __init__(self, host, port, vhost, username, password):
        self.host = host
        self.port = port
        self.vhost = vhost
        self.username = username
        self.password = password

        credentials = pika.PlainCredentials(self.username, self.password)

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port, virtual_host=self.vhost , credentials=credentials))
        
        self.channel = connection.channel()

        self.channel.exchange_declare(exchange='BOTS_MESSAGES', exchange_type='direct', durable=True)
        
        channel.queue_bind(exchange=exchange_name,
                   queue=queue_name,
                   routing_key='black')

        self.channel.exchange_declare(exchange='CC_MESSAGES', exchange_type='direct', durable=True)

        self.task_manager = Task()

        print('--------------- Connection Established ---------------')
        print()

    def receive(self, q):
        self.queue = q
        self.channel.queue_declare(queue=self.queue)
        
        print(' [*] Waiting for MESSAGES. To exit press CTRL+C')

        def callback(ch, method, properties, body):
            message = json.loads(body)
            self.task_manager.menu(message['type'], message)
            #Make sure no mistake is made
            time.sleep(20)

        self.channel.basic_consume(queue=self.queue, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def send(self, exchange, routing_key, message):
        channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))

if __name__ == "__main__":
    rabbit = Rabbitmq(host='mqtt-redesfis.5g.cn.atnog.av.it.pt', port=5672, vhost="PI",username='pi_rabbit_admin', password='yPvawEVxks7MLg3lfr3g')
    rabbit.receive(q='API')
