import time
from datetime import datetime
import json
import pickle


# -----------------------------------------------------------
# json
# -----------------------------------------------------------

def to_json(obj):
	return json.dumps(obj, separators=(',', ':'))


def from_json(string):
	return json.loads(string)


def wait(seconds: float):
	time.sleep(seconds)


def current_time(str_time=False):
	if str_time:
		return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	return datetime.utcnow().timestamp()


def read_model(models, label):
	result = models.find_one({'label': label}, {'_id': 0})
	return result['config'], pickle.loads(result['model']), pickle.loads(result['tokenizer'])


def get_labels(models, policy_label):
	return [result['label'] for result in models.find({'label': {'$in': policy_label}}, {'_id': 0})]
