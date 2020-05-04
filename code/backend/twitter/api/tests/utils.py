import functools
import subprocess
import pytest


def catch_exception(func):
	"""

	Returns:
		object: 
	"""
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		worker = kwargs['error_catcher']
		try:
			return func(*args, **kwargs)
		except Exception as e:
			print('stdout:', worker.stdout.read().decode("utf-8"))
			print('stderr:', worker.stderr.read().decode("utf-8"))
			raise

	return wrapper


@pytest.fixture(scope='module')
def error_catcher(request) -> subprocess.Popen:
	"""py.test fixture to create app scaffold."""
	cmdline = ["echo", "ERROR!!"]

	worker = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	worker.wait(timeout=5.0)

	return worker


def is_keys_in_data(response_data, data_keys=None):
	if data_keys is None:
		return True
	return all(key in data_keys for key in response_data)


def is_response_successful(response):
	return response.status_code == 200 and len(response.data['error_messages']) == 0 and \
		   len(response.data['success_messages']) > 0 and response.data['data'] != []


def is_response_unsuccessful(response):
	return response.status_code == 403 and len(response.data['error_messages']) > 0 and \
		   len(response.data['success_messages']) == 0


def is_response_empty(response):
	return response.status_code == 200 and len(response.data['error_messages']) == 0 and \
		   len(response.data['success_messages']) > 0 and response.data['data'] == []


def is_response_successful_with_pagination(response, entries_per_page=None):
	return response.status_code == 200 and len(response.data['error_messages']) == 0 and \
		   len(response.data['success_messages']) > 0 and response.data['data']['entries'] != [] and \
		   (entries_per_page is None or len(response.data['data']['entries']) == entries_per_page)


def is_response_empty_with_pagination(response):
	return response.status_code == 200 and len(response.data['error_messages']) == 0 and \
		   len(response.data['success_messages']) > 0 and response.data['data']['entries'] == []
