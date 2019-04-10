from typing import Tuple

import utils
from exceptions import NoMessagesInQueue


class MessagingWrapper:
    def __init__(self, *, host="127.0.0.1", port="80", vhost="%2f", auth: Tuple):
        self.endpoint = f"http://{host}:{port}/api/"
        self.vhost = vhost
        self.auth = auth
        pass

    def _make_request(self, method, url, data, **kwargs):
        return utils.make_request_json(method, url=url, data=data, auth=self.auth, **kwargs)

    def create_queue(self, name):
        url = f"{self.endpoint}queues/{self.vhost}/{name}"
        options = {
            "durable"    : "true",
            "auto_delete": False,
        }
        self._make_request('put', url=url, data=options)

    def create_direct_exchange(self, name):
        url = f"{self.endpoint}exchanges/{self.vhost}/{name}"
        options = {
            "type"   : "direct",
            "durable": True
        }
        self._make_request('put', url=url, data=options)

    def bind_queue_to_exchange(self, exchange, queue, **kwargs):
        url = f"{self.endpoint}exchanges/{self.vhost}/e/{exchange}/q/{queue}"
        self._make_request('post', url, data=kwargs)

    def get_next_message(self, queue):
        url = f"{self.endpoint}queues/{self.vhost}/{queue}/get"
        options = {
            "count"   : 1,
            "ackmode" : "ack_requeue_false",
            "encoding": "auto",
        }
        res = self._make_request('post', url, data=options)
        if res:
            return res
        raise NoMessagesInQueue("Queue has no messages left!")

    def publish_message(self, exchange, data):
        url = f"{self.endpoint}exchanges/{self.vhost}/{exchange}/publish"
        options = {
            "properties"      : {},
            "routing_key"     : "my key",
            "payload"         : utils.to_json(data),
            "payload_encoding": "string"
        }
        self._make_request('post', url=url, data=options)
