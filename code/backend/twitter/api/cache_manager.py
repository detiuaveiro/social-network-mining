import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
django.setup()

import redis
from credentials import REDIS_URL
import pickle
from api.queries import *


class RedisAPI:
	def __init__(self):
		self.client = redis.Redis(host=REDIS_URL, db=1)

	def set(self, key, value):
		return self.client.set(key, pickle.dumps(value))

	def key_exists(self, key):
		return self.client.exists(key)

	def get(self, key):
		return pickle.loads(self.client.get(key))

	def delete_key(self, key):
		return self.client.delete(key)

	def update_per_table(self, model_name):
		keys = filter(lambda k: model_name == k['model_name'], map(lambda k: pickle.loads(k), self.client.scan_iter()))

		for key in keys:
			encoded_key = pickle.dumps(key)
			data = self.get(encoded_key)
			self.delete_key(encoded_key)
			func = eval(f"{key['function_name']}")
			status, data, message = func(*key['args'])

			if status:
				new_data = {
					'data': data,
					'message': message
				}

				self.set(encoded_key, new_data)
			else:
				self.set(encoded_key, data)


cacheAPI = RedisAPI()
