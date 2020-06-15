import functools
import pickle

import api.cache_manager


def cache(model_name, pagination=False):
	def decorator_cache(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):

			function_name = func.__name__
			key_data = {
				'model_name': model_name,
				'args': args,
				'kwargs': kwargs,
				'function_name': function_name
			}

			key = pickle.dumps(key_data)

			if api.cache_manager.cacheAPI.key_exists(key):
				value = api.cache_manager.cacheAPI.get(key)
				status, data, message = True, value['data'], value['message']
			else:
				status, data, message = func(*args, **kwargs)
				value = {
					'data': data,
					'message': message,
					'pagination': pagination
				}

				if status and 'last_id' not in kwargs:
					api.cache_manager.cacheAPI.set(key, value)

			return status, data, message

		return wrapper

	return decorator_cache
