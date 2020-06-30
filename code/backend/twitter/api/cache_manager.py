import redis
from credentials import REDIS_URL, REDIS_PORT
import pickle


class RedisAPI:
    def __init__(self):
        self.client = redis.Redis(host=REDIS_URL, db=1, port=REDIS_PORT)

    def set(self, key, value):
        return self.client.set(key, pickle.dumps(value))

    def key_exists(self, key):
        return self.client.exists(key)

    def get(self, key):
        v = self.client.get(key)
        if v:
            return pickle.loads(v)
        return None

    def delete_key(self, key):
        return self.client.delete(key)

    def delete_all_keys(self):
        return self.client.flushall()
