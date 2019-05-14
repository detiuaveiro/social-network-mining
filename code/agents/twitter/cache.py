import json
from json import JSONEncoder
from typing import Any, Dict, Optional

from models import User, Tweet


def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)


_default.default = JSONEncoder().default
JSONEncoder.default = _default


class Cache:
    """
    Simple JSON-like storage
    """

    def __init__(self, filename, *, logger):
        self._file_name = filename
        self._file = None
        self._logger = logger
        self._cache: Dict[Any]
        self._closed = True

    def open(self):
        cache_file_name = f"{self._file_name}.json"
        self._closed = False
        try:
            self._file = open(cache_file_name, "r+", encoding="utf8")
            self._cache = json.load(self._file)
        except FileNotFoundError:
            self._logger.debug(f"Cache file not found. Creating with name «{cache_file_name}»")
            self._cache = {}
            self._file = open(cache_file_name, "w+", encoding="utf8")
            self._flush()
        # Initializing for users and tweets
        if not self._cache.get("users", None):
            self._cache["users"] = {}

        if not self._cache.get("tweets", None):
            self._cache["tweets"] = {}

    def _flush(self):
        if self._closed:
            self._logger.error("ERROR: Trying to flush closed file")
            return
        self._file.seek(0)
        json.dump(obj=self._cache, fp=self._file)
        self._file.flush()

    def set(self, key: str, value: Any) -> None:
        if self._closed:
            self._logger.error("ERROR: Trying to write to closed file")
            return
        self._cache[key] = value
        self._flush()

    def get(self, key: str, val=None) -> Optional[Any]:
        return self._cache.get(key, val)

    def save_tweet(self, tweet_obj: Tweet):
        self._cache["tweets"][tweet_obj.id] = tweet_obj.to_json()
        self._flush()

    def save_user(self, user_obj: User):
        self._cache["users"][user_obj.id] = user_obj
        self._flush()

    def get_user(self, user_obj: User) -> Optional[User]:
        return self._cache.get("users", {}).get(user_obj.id, None)

    def get_tweet(self, tweet_obj: Tweet) -> Optional[Tweet]:
        return self._cache.get("tweets", {}).get(tweet_obj.id, None)

    def close(self):
        if self._closed:
            self._logger.error("ERROR: No open file to close!")
            return
        self._flush()
        self._file.close()
