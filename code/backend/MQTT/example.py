from pyrabbit2 import Client
import json

#Establishes Connection
cl = Client('mqtt-redesfis.ws.atnog.av.it.pt:80','pi_rabbit_admin', 'yPvawEVxks7MLg3lfr3g')

#Creates vhost, not mandatory but peanuts
cl.create_vhost('PI')

#Creates exchange, not mandatory but peanuts
cl.create_exchange(vhost='PI', name='BOTS_MESSAGES', xtype='direct')

#Creates queue, not mandatory but peanuts
cl.create_queue(vhost='PI', name='API')

#Creates binding, not mandatory but peanuts
cl.create_binding(vhost='PI', exchange='BOTS_MESSAGES', queue='API', rt_key='API')


#Example of an message
body={
<<<<<<< HEAD
    "type":7,
    "data":{
        "id": 1122,
        "text": "texto 12345",
    },
=======
    "type":1,
    "text":"sajnddjsa",
>>>>>>> Rabbitmq http api example
    }
#send message
cl.publish('PI', 'BOTS_MESSAGES', 'API', payload=json.dumps(body),payload_enc='string')

<<<<<<< HEAD
class MessagingWrapper:
    def __init__(self, host, port, vhost, username, password):
        self.host = host
        self.port = port
        self.vhost = vhost
        self.username = username
        self.password = password
        self.url = self.host+":"+self.port
        #Establishes Connection
        cl = Client(self.url,self.username,self.password)

        #Creates vhost, not mandatory but peanuts
        cl.create_vhost(self.vhost)
    
    def get_messages(self, queue):
        

    def publish(self, queue, exchange, data):
        self.queue = queue
        self.exchange = exchange
        #Creates exchange, not mandatory but peanuts
        cl.create_exchange(vhost=self.vhost, name=self.exchange, xtype='direct')

        #Creates queue, not mandatory but peanuts
        cl.create_queue(vhost=self.vhost, name=self.queue)

        #Creates binding, not mandatory but peanuts
        cl.create_binding(vhost='PI', exchange=self.exchange, queue=self.queue, rt_key='API')

        #Example of an message
        """ body={
            "type":7,
            "data":{
                "id": 1122,
                "text": "texto 12345",
            },
        } """
        #send message
        cl.publish(self.vhost, self.exchange, self.queue, payload=json.dumps(data), payload_enc='string')


=======
#receive messages
print(cl.get_messages('PI', 'API'))
>>>>>>> Rabbitmq http api example
