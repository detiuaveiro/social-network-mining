from stompest.config import StompConfig
from stompest.protocol import StompSpec
from stompest.sync import Stomp

CONFIG = StompConfig('tcp://mqtt-redesfis.ws.atnog.av.it.pt:443')
QUEUE = '/queue/test'

if __name__ == '__main__':
    client = Stomp(CONFIG)
    client.connect()
    client.subscribe(QUEUE, {StompSpec.ACK_HEADER: StompSpec.ACK_CLIENT_INDIVIDUAL})
    while True:
        frame = client.receiveFrame()
        print('Got %s' % frame.info())
        client.ack(frame)
    client.disconnect()