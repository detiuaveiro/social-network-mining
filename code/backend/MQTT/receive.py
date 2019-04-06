import requests
import json

url="http://mqtt-redesfis.ws.atnog.av.it.pt:80/api/queues/%2f/API/get"

auth=('pi_rabbit_admin', 'yPvawEVxks7MLg3lfr3g')

body={"count":1,"ackmode":"ack_requeue_false","encoding":"auto"}

response = requests.post(url=url, auth=auth, data=json.dumps(body))

print(response)