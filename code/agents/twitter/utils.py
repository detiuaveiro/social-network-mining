from datetime import datetime
import json


# -----------------------------------------------------------
# json
# -----------------------------------------------------------

def to_json(obj):
    return json.dumps(obj, separators=(',', ':'))


def from_json(string):
    return json.loads(string)


def current_time(str_time=False):
    if str_time:
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return datetime.utcnow().timestamp()
