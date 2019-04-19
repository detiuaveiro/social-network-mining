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
    "type":7,
    "data":{
        "id": 1122,
        "text": "texto 12345",
    },
    }
#send message
cl.publish('PI', 'BOTS_MESSAGES', 'API', payload=json.dumps(body),payload_enc='string')

