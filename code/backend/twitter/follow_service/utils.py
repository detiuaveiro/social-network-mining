import time
from datetime import datetime
import json
import pickle
import re


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


def get_full_text(data):
	text = []

	for entry in data:
		if 'retweeted_status' in entry:
			text.append(entry['retweeted_status']['full_text'])

		else:
			text.append(entry['full_text'])

		text[-1] = re.sub(r"http\S+", "", text[-1])
		text[-1] = re.sub(' +', ' ', text[-1])
	return text


def read_model(models, label):
	result = models.find_one({'label': label}, {'_id': 0})
	return result['config'], pickle.loads(result['model']), pickle.loads(result['tokenizer'])


def get_labels(models, policy_label):
	return [result['label'] for result in models.find({'label': {'$in': policy_label}}, {'_id': 0})]


def convert_policies_to_model_input_data(policies):
	training_data = {}
	for policy in policies:
		params = policy['params']
		label = policy['name']
		training_data[label] = params

	return training_data


def update_models(models, data, labels):
	for tokenizer, model, config, label in data:
		models.update_one({'label': label}, {'$set': {
			'label': label,
			'args': labels[label],
			'tokenizer': pickle.dumps(tokenizer, protocol=pickle.HIGHEST_PROTOCOL),
			'model': pickle.dumps(model.model, protocol=pickle.HIGHEST_PROTOCOL),
			'config': config
		}}, upsert=True)


def update_tweets(policies_tweets_model, policies_tweets):
	for policy_name, tweets in policies_tweets.items():
		policies_tweets_model.update_one({'name': policy_name}, {'$set': {
			'name': policy_name,
			'tweets': tweets
		}}, upsert=True)
