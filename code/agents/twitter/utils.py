import json
import random
import datetime

TWITTER_EPOCH = 1288834974657


def to_json(obj):
    return json.dumps(obj, separators=(',', ':'))


def from_json(string):
    return json.loads(string)


def random_between(min_val, max_val):
    return random.randint(min_val, max_val)


def snowflake_time(id: int) -> datetime.datetime:
    """Returns the creation date in UTC of a Twitter id."""
    return datetime.datetime.utcfromtimestamp(((id >> 22) + TWITTER_EPOCH) / 1000)