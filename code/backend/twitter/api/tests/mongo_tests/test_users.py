import pytest
from django.test import RequestFactory
from django.urls import reverse
from api.models import User, Tweet
from api.views import users
from mixer.backend.django import mixer
from api.tests.utils import *


@pytest.fixture(scope='module')
def factory():
	return RequestFactory()


@pytest.fixture
def users_list(db):
	return mixer.cycle(20).blend(User, name="user1", screen_name="user2")


@pytest.fixture
def user(db):
	return mixer.blend(User, id="1", user_id="1")


@pytest.fixture
def tweets(db):
	return mixer.cycle(20).blend(Tweet, user="1")


@catch_exception
def test_successful_twitter_users_count_request(error_catcher, factory, users_list):
	path = reverse('twitter_users_count')
	request = factory.get(path)
	response = users.twitter_users_count(request)
	assert is_response_successful(response) and response.data['data']['count'] == len(users_list)


@catch_exception
def test_empty_twitter_users_count_request(error_catcher, factory, db):
	path = reverse('twitter_users_count')
	request = factory.get(path)
	response = users.twitter_users_count(request)
	assert response.data['data']['count'] == 0 and response.status_code == 200


@catch_exception
def test_successful_twitter_users_request(error_catcher, factory, users_list):
	path = reverse('twitter_users')
	request = factory.get(path)
	response = users.twitter_users(request)
	assert is_response_successful_with_pagination(response, len(users_list))


@catch_exception
def test_successful_twitter_users_request_with_pagination(error_catcher, factory, users_list):
	path = reverse('twitter_users', kwargs={'entries_per_page': 10, 'page': 1})
	request = factory.get(path)
	response = users.twitter_users(request, entries_per_page='10', page='1')
	assert is_response_successful_with_pagination(response, 10)


@catch_exception
def test_empty_twitter_users_request(error_catcher, factory, db):
	path = reverse('twitter_users')
	request = factory.get(path)
	response = users.twitter_users(request)
	assert is_response_empty_with_pagination(response)


@catch_exception
def test_unsuccessfully_twitter_users_request_with_pagination(error_catcher, factory, users_list):
	path = reverse('twitter_users', kwargs={'entries_per_page': 0, 'page': 1})
	request = factory.get(path)
	response = users.twitter_users(request, entries_per_page='0', page='1')
	assert is_response_unsuccessful(response)


@catch_exception
def test_successful_twitter_user_request(error_catcher, factory, user):
	path = reverse('twitter_user', kwargs={'user_id': 1})
	request = factory.get(path)
	response = users.twitter_user(request, user_id="1")
	assert is_response_successful(response)


@catch_exception
def test_unsuccessfully_twitter_user_request(error_catcher, factory, db):
	path = reverse('twitter_user', kwargs={'user_id': 1})
	request = factory.get(path)
	response = users.twitter_user(request, user_id="1")
	assert is_response_unsuccessful(response)


@catch_exception
def test_successful_twitter_user_tweets_request(error_catcher, factory, tweets):
	path = reverse('twitter_user_tweets', kwargs={'user_id': 1})
	request = factory.get(path)
	response = users.twitter_user_tweets(request, user_id="1")
	assert is_response_successful_with_pagination(response, len(tweets))


@catch_exception
def test_successful_twitter_user_tweets_request_with_pagination(error_catcher, factory, tweets):
	path = reverse('twitter_user_tweets', kwargs={'user_id': 1, 'entries_per_page': 10, 'page': 1})
	request = factory.get(path)
	response = users.twitter_user_tweets(request, user_id="1", entries_per_page='10', page='1')
	assert is_response_successful_with_pagination(response, 10)


@catch_exception
def test_empty_twitter_user_tweets_request(error_catcher, factory, db):
	path = reverse('twitter_user_tweets', kwargs={'user_id': "1"})
	request = factory.get(path)
	response = users.twitter_user_tweets(request, user_id="1")
	assert is_response_empty_with_pagination(response)


@catch_exception
def test_unsuccessfully_twitter_user_tweets_request_with_pagination(error_catcher, factory, tweets):
	path = reverse('twitter_user_tweets', kwargs={'user_id': 1, 'entries_per_page': 0, 'page': 1})
	request = factory.get(path)
	response = users.twitter_user_tweets(request, user_id="1", entries_per_page='0', page='1')
	assert is_response_unsuccessful(response)


@catch_exception
def test_successful_twitter_search_users_request(error_catcher, factory, users_list):
	path = reverse('twitter_search_users', kwargs={'keywords': "user"})
	request = factory.get(path)
	response = users.twitter_search_users(request, keywords="user")
	assert is_response_successful_with_pagination(response, len(users_list))


@catch_exception
def test_successful_twitter_search_users_request_with_pagination(error_catcher, factory, users_list):
	path = reverse('twitter_search_users', kwargs={'keywords': "user", 'entries_per_page': 10, 'page': 1})
	request = factory.get(path)
	response = users.twitter_search_users(request, keywords="user", entries_per_page='10', page='1')
	assert is_response_successful_with_pagination(response, 10)


@catch_exception
def test_empty_twitter_search_users_tweets_request(error_catcher, factory, db):
	path = reverse('twitter_search_users', kwargs={'keywords': "user"})
	request = factory.get(path)
	response = users.twitter_search_users(request,  keywords="user")
	assert is_response_empty_with_pagination(response)


@catch_exception
def test_unsuccessfully_twitter_search_users_request_with_pagination(error_catcher, factory, users_list):
	path = reverse('twitter_search_users', kwargs={'keywords': "user", 'entries_per_page': 0, 'page': 1})
	request = factory.get(path)
	response = users.twitter_search_users(request,  keywords="user", entries_per_page='0', page='1')
	assert is_response_unsuccessful(response)
