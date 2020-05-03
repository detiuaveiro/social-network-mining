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
def tweets_stats(db):
	return mixer.cycle(20).blend(TweetStats)


@pytest.fixture
def tweet_stats(db):
	return mixer.cycle(20).blend(TweetStats, tweet_id=1)


@catch_exception
def test_successful_twitter_tweets_stats_request(error_catcher, factory, tweets_stats):
	path = reverse('twitter_tweets_stats')
	request = factory.get(path)
	response = tweets.twitter_tweets_stats(request)
	assert is_response_successful_with_pagination(response, len(tweets_stats))


@catch_exception
def test_successful_twitter_tweets_stats_request_with_pagination(error_catcher, factory, tweets_stats):
	path = reverse('twitter_tweets_stats', kwargs={'entries_per_page': 10, 'page': 1})
	request = factory.get(path)
	response = tweets.twitter_tweets_stats(request, entries_per_page=10, page=1)
	assert is_response_successful_with_pagination(response, 10)


@catch_exception
def test_empty_twitter_tweets_stats_request(error_catcher, factory, db):
	path = reverse('twitter_tweets_stats')
	request = factory.get(path)
	response = tweets.twitter_tweets_stats(request)
	assert is_response_empty_with_pagination(response)


@catch_exception
def test_unsuccessfully_twitter_tweets_stats_request_with_pagination(error_catcher, factory, tweets_stats):
	path = reverse('twitter_tweets_stats', kwargs={'entries_per_page': 0, 'page': 1})
	request = factory.get(path)
	response = tweets.twitter_tweets_stats(request, entries_per_page=0, page=1)
	assert is_response_unsuccessful(response)


@catch_exception
def test_successful_twitter_tweet_stats_request(error_catcher, factory, tweet_stats):
	path = reverse('twitter_tweet_stats', kwargs={'tweet_id': 1})
	request = factory.get(path)
	response = tweets.twitter_tweet_stats(request, tweet_id=1)
	assert is_response_successful_with_pagination(response, len(tweet_stats))


@catch_exception
def test_successful_twitter_tweet_stats_request_with_pagination(error_catcher, factory, tweet_stats):
	path = reverse('twitter_tweet_stats', kwargs={'tweet_id': 1, 'entries_per_page': 10, 'page': 1})
	request = factory.get(path)
	response = tweets.twitter_tweet_stats(request, tweet_id=1, entries_per_page=10, page=1)
	assert is_response_successful_with_pagination(response, 10)


@catch_exception
def test_empty_twitter_tweet_stats_request(error_catcher, factory, db):
	path = reverse('twitter_tweet_stats', kwargs={'tweet_id': 1})
	request = factory.get(path)
	response = tweets.twitter_tweet_stats(request, tweet_id=1)
	assert is_response_empty_with_pagination(response)


@catch_exception
def test_unsuccessfully_twitter_tweet_stats_request_with_pagination(error_catcher, factory, tweet_stats):
	path = reverse('twitter_tweet_stats', kwargs={'tweet_id': 1, 'entries_per_page': 0, 'page': 1})
	request = factory.get(path)
	response = tweets.twitter_tweet_stats(request, tweet_id=1, entries_per_page=0, page=1)
	assert is_response_unsuccessful(response)
