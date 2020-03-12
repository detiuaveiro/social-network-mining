import pytest
from django.test import RequestFactory
from django.urls import reverse
from api.models import TweetStats
from api.views import tweets
from mixer.backend.django import mixer
from api.tests.utils import *


@pytest.fixture(scope='module')
def factory():
    return RequestFactory()


@pytest.fixture
def tweet(db):
    return mixer.blend(Tweet)


@pytest.fixture
def tweets_list(db):
    return mixer.cycle(5).blend(Tweet)


@pytest.fixture
def tweets_stats(db):
    return mixer.cycle(5).blend(TweetStats)


@pytest.fixture
def tweet_stats(db):
    return mixer.blend(TweetStats, tweet_id=1)


def test_successful_twitter_tweets_stats_request(factory, tweets_stats):
    path = reverse('twitter_tweets_stats')
    request = factory.get(path)
    response = tweets.twitter_tweets_stats(request)
    assert is_response_successful(response)


def test_unsuccessfully_twitter_tweets_stats_request(factory, db):
    path = reverse('twitter_tweets_stats')
    request = factory.get(path)
    response = tweets.twitter_tweets_stats(request)
    assert is_response_empty(response)


def test_successful_twitter_tweet_stats_request(factory, tweet_stats):
    path = reverse('twitter_tweet_stats', kwargs={'id': 1})
    request = factory.get(path)
    response = tweets.twitter_tweet_stats(request, id=1)
    assert is_response_successful(response)


def test_unsuccessfully_twitter_tweet_stats_request(factory, db):
    path = reverse('twitter_tweet_stats', kwargs={'id': 1})
    request = factory.get(path)
    response = tweets.twitter_tweet_stats(request, id=1)
    assert is_response_unsuccessful(response)
