import pika
import json
## Excuse me what?
# Did they deadass make a class just to send shit?
# Literally why tho
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
            exchange="tasks_deliver",
            routing_key=routing_key,
            body=json.dumps(message)
            )
    def close(self):
        self.connection.close()