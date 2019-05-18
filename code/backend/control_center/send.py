import pika
import json
class RabbitSend():
    def __init__(self, host, port, vhost, username, password):
        self.host = host
        self.port = port
        self.vhost = vhost
        self.username = username
        self.password = password

        credentials = pika.PlainCredentials(self.username, self.password)

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port, virtual_host=self.vhost , credentials=credentials))
        
        self.channel = self.connection.channel()

    def send(self, routing_key, message):
        self.channel.basic_publish(
            exchange="task_deliver",
            routing_key=routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=1,  # make message persistent
            ))
    def close(self):
        self.connection.close()