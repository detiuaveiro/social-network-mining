import json


def to_json(obj):
    return json.dumps(obj, separators=(',', ':'))


def from_json(string):
    return json.loads(string)
