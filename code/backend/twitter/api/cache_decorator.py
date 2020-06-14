import functools
import pickle

import api.cache_manager


def cache(model_name):
	def decorator_cache(func):
		@functools.wraps(func)
		def wrapper(*args):
			function_name = func.__name__
			key_data = {
				'model_name': model_name,
				'args': args,
				'function_name': function_name
			}
			key = pickle.dumps(key_data)

			if api.cache_manager.cacheAPI.key_exists(key):
				value = api.cache_manager.cacheAPI.get(key)
				status, data, message = True, value['data'], value['message']
			else:
				status, data, message = func(*args)
				value = {
					'data': data,
					'message': message
				}

				if status:
					api.cache_manager.cacheAPI.set(key, value)

			return status, data, message

		return wrapper

	return decorator_cache
