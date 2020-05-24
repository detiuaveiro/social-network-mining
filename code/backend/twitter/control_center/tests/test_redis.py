import redis
import json
import time

r = redis.Redis()


def to_json(data: dict) -> str:
	return json.dumps(data, separators=(',', ':'))


def test_redis_ttl():
	data = {
		'type': 'message_type',
		'data': ['data', 'lel']
	}
	r.set(to_json(data), "")
	r.expire(to_json(data), 1)

	time.sleep(1)
	if r.get(to_json):
		return "Something went wrong"

	return "Everything's good"