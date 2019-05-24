import datetime
import json
import random
import time

import readtime
import requests

from enums import MessageType

TWITTER_EPOCH = 1288834974657


def to_json(obj):
    return json.dumps(obj, separators=(',', ':'))


def from_json(string):
    return json.loads(string)


def random_between(min_val, max_val):
    return random.uniform(min_val, max_val)


def snowflake_time(id: int) -> datetime.datetime:
    """Returns the creation date in UTC of a Twitter id."""
    return datetime.datetime.utcfromtimestamp(((id >> 22) + TWITTER_EPOCH) / 1000)


def wait_for(secs):
    """Uses time.sleep to wait for a specified amount of seconds"""
    time.sleep(secs)


def read_text_and_wait(text: str):
    """
    Fakes the reading time for the given text.

    Parameters
    ----------
    text : str
        text to read

    Returns
    -------
    the time taken to read the text provided

    """
    time_for_text = readtime.of_text(text)
    # edge case if it was empty 
    # TODO: Don't forget to check for entities and etc
    time_for_text = time_for_text.seconds if time_for_text.seconds > 1 else 1

    # wait for the some time
    wait_time = random_between(time_for_text * 0.9, time_for_text * 1.10)
    # wait the given time

    wait_for(round(wait_time))

    # handy return for keeping track of the total times
    return wait_time


def current_time():
    return datetime.datetime.utcnow().timestamp()


def make_request_json(method, url, data, **options):
    return requests.request(method=method, url=url, data=to_json(data), **options)


def wrap_message(data, *, bot_id, message_type: MessageType):
    payload = {
        "type"     : message_type,
        "bot_id"   : bot_id,
        "timestamp": current_time(),
        "data"     : data,
    }
    return payload
