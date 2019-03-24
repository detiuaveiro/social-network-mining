import json
import pika


class PEP:

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='hello')
        self.channel.start_consuming()
        return
    
    def callback(self,ch, method, properties, body):
        print(" [x] Received %r" % body)
    

    def receive_amqp_message(self):
        self.channel.basic_consume(self.callback,
                      queue='hello',
                      no_ack=True)

        return

    def formulate_request(self):
        return

    def send_request(self):
        #json dumps do formulate_request()
        return
    
    def receive_response(self):
        #json loads da resposta do PDP
        return
    
    def enforce(self): #send_amqp_message(self) probably more suitable...

        #get response and enforce it
        self.channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
        return

    def close_connection(self):
        self.connection.close()
