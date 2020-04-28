import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.setsockopt(zmq.LINGER, 1)
host = 'tcp://{}:{}'.format('localhost', 5555)
socket.connect(host)

message = {
	'id': 'bots',
	'text': "I can't take this quarantine anymore, I'm giving up silly with nothing to do",
	'episode_done': False,
}

text = json.dumps(message)
socket.send_unicode(text)
reply = socket.recv_unicode()
print(reply)

socket.close()
