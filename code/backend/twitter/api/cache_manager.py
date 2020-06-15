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
			func = eval(f"{key['function_name']}")
			self.delete_key(encoded_key)

			if data['pagination']:
				status, n_data, message = func(*key['args'], **key['kwargs'])

				if status:
					new_data = {
						'data': n_data,
						'message': message
					}

					self.set(encoded_key, new_data)
				else:
					self.set(encoded_key, data)

			else:
				last_id = data['data']['last_id']
				key['kwargs']['last_id'] = last_id

				status, n_data, message = func(*key['args'], **key['kwargs'])
				if status:
					entries_dict = {}
					for entry in data['data']['entries']:
						entries_dict[entry.pop('date')] = entry

					for entry in n_data['entries']:
						date = entry.pop('date')
						general = entry

						if date not in entries_dict:
							empty_counter = {}
							for entity in general:
								empty_counter[entity] = 0
							entries_dict[date] = empty_counter

						current_counter = entries_dict[date]
						for entity in current_counter:
							current_counter[entity] += general[entity]
						entries_dict[date] = current_counter

					entries = []
					for date in entries_dict:
						entries.append({
							**entries_dict[date],
							'date': date
						})

					new_data = {
						'message': data['message'],
						'data': {
							'last_id': n_data['last_id'],
							'entries': entries
						},
						'pagination': False
					}

					self.set(encoded_key, new_data)
				else:
					self.set(encoded_key, data)


cacheAPI = RedisAPI()
