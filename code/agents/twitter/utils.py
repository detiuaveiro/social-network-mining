import json
import random

def to_json(obj):
    return json.dumps(obj, separators=(',', ':'))


def from_json(string):
    return json.loads(string)

def random_delay(min_val, max_val):
	return random.randint(min_val, max_val)