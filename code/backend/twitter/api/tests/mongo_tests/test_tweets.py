import pytest
from django.test import RequestFactory
from django.urls import reverse
from api.models import Tweet
from api.views import tweets
from mixer.backend.django import mixer
from api.tests.utils import *


@pytest.fixture(scope='module')
def factory():
	return RequestFactory()


@pytest.fixture
def tweet(db):
	return mixer.blend(Tweet, tweet_id="1", in_reply_to_status_id_str="1", user={'id': 1, 'name': 'user'})


@pytest.fixture
def tweets_list(db):
	return mixer.cycle(20).blend(Tweet, user={'id': 1, 'name': 'user'})


@catch_exception
def test_successful_twitter_tweets_request(error_catcher, factory, tweets_list):
	path = reverse('twitter_tweets')
	request = factory.get(path)
	response = tweets.twitter_tweets(request)
	assert is_response_successful_with_pagination(response, len(tweets_list))


@catch_exception
def test_successful_twitter_tweets_request_with_pagination(error_catcher, factory, tweets_list):
	path = reverse('twitter_tweets', kwargs={'entries_per_page': 10, 'page': 1})
	request = factory.get(path)
	response = tweets.twitter_tweets(request, entries_per_page=10, page=1)
	assert is_response_successful_with_pagination(response, 10)


@catch_exception
def test_empty_twitter_tweets_request(error_catcher, factory, db):
	path = reverse('twitter_tweets')
	request = factory.get(path)
	response = tweets.twitter_tweets(request)
	assert is_response_empty_with_pagination(response)


@catch_exception
def test_unsuccessfully_twitter_tweets_request(error_catcher, factory, tweets_list):
	path = reverse('twitter_tweets', kwargs={'entries_per_page': 0, 'page': 1})
	request = factory.get(path)
	response = tweets.twitter_tweets(request, entries_per_page=0, page=1)
	assert is_response_unsuccessful(response)


@catch_exception
def test_successful_twitter_tweet_request(error_catcher, factory, tweet):
	path = reverse('twitter_tweet', kwargs={'tweet_id': "1"})
	request = factory.get(path)
	response = tweets.twitter_tweet(request, tweet_id="1")
	assert is_response_successful(response)


@catch_exception
def test_unsuccessfully_twitter_tweet_request(error_catcher, factory, db):
	path = reverse('twitter_tweet', kwargs={'tweet_id': "1"})
	request = factory.get(path)
	response = tweets.twitter_tweet(request, tweet_id="1")
	assert is_response_unsuccessful(response)


@catch_exception
def test_successful_twitter_tweet_replies_request(error_catcher, factory, tweet):
	path = reverse('twitter_tweet_replies', kwargs={'tweet_id': "1"})
	request = factory.get(path)
	response = tweets.twitter_tweet_replies(request, tweet_id="1")
	assert is_response_successful(response)


@catch_exception
def test_unsuccessfully_twitter_tweet_replies_request(error_catcher, factory, db):
	path = reverse('twitter_tweet_replies', kwargs={'tweet_id': "1"})
	request = factory.get(path)
	response = tweets.twitter_tweet_replies(request, tweet_id="1")
	assert is_response_empty(response)
