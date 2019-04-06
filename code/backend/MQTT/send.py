import requests
import json

url="http://mqtt-redesfis.ws.atnog.av.it.pt:80/api/exchanges/%2f/amq.default/publish"

auth=('pi_rabbit_admin', 'yPvawEVxks7MLg3lfr3g')

body={
    "properties":{},
    "routing_key":"API",
    "payload":"message test 2",
    "payload_encoding":"string"
    }

response = requests.post(url=url, auth=auth, data=json.dumps(body))

print(response)