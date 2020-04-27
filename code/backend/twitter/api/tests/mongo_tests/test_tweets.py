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
    return mixer.blend(Tweet, tweet_id=1, in_reply_to_status_id=1)


@pytest.fixture
def tweets_list(db):
    return mixer.cycle(5).blend(Tweet)


@catch_exception
def test_successful_twitter_tweets_request(error_catcher, factory, tweets_list):
    path = reverse('twitter_tweets')
    request = factory.get(path)
    response = tweets.twitter_tweets(request)
    assert is_response_successful(response)


@catch_exception
def test_successful_twitter_tweets_with_limit_request(error_catcher, factory, tweets_list):

    path = reverse('twitter_tweets',)
    request = factory.get(path)
    response = tweets.twitter_tweets(request)
    assert is_response_successful(response)


@catch_exception
def test_unsuccessfully_twitter_tweets_request(error_catcher, factory, db):
    path = reverse('twitter_tweets')
    request = factory.get(path)
    response = tweets.twitter_tweets(request)
    assert is_response_unsuccessful(response)


@catch_exception
def test_successful_twitter_tweet_request(error_catcher, factory, tweet):
    path = reverse('twitter_tweet', kwargs={'id': 1})
    request = factory.get(path)
    response = tweets.twitter_tweet(request, id=1)
    assert is_response_successful(response)


@catch_exception
def test_unsuccessfully_twitter_tweet_request(error_catcher, factory, db):
    path = reverse('twitter_tweet', kwargs={'id': 1})
    request = factory.get(path)
    response = tweets.twitter_tweet(request, id=1)
    assert is_response_unsuccessful(response)


@catch_exception
def test_successful_twitter_tweet_replies_request(error_catcher, factory, tweet):
    path = reverse('twitter_tweet_replies', kwargs={'id': 1})
    request = factory.get(path)
    response = tweets.twitter_tweet_replies(request, id=1)
    assert is_response_successful(response)


@catch_exception
def test_unsuccessfully_twitter_tweet_replies_request(error_catcher, factory, db):
    path = reverse('twitter_tweet_replies', kwargs={'id': 1})
    request = factory.get(path)
    response = tweets.twitter_tweet_replies(request, id=1)
    assert is_response_unsuccessful(response)
