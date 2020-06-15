import pytest
from django.test import RequestFactory
from django.urls import reverse
from api.models import User, Tweet
from api.views import users
from mixer.backend.django import mixer
from api.tests.utils import *
from api import neo4j


@pytest.fixture(autouse=True)
def delete_neo4j_data():
	for id in ["1", "2", "3"]:
		neo4j.delete_bot(id)
		neo4j.delete_tweet(id)
		if neo4j.check_bot_exists(id):
			return False
		if neo4j.check_tweet_exists(id):
			return False
	return True


def add_bot_neo4j(list_id):
	for id in list_id:
		neo4j.add_bot({'id': id, 'name': 'bot_test', 'username': 'bot_test_username'})
		neo4j.save_all
		if not neo4j.check_bot_exists(id):
			return False
	return True


def add_tweet_neo4j(list_id):
	for id in list_id:
		neo4j.add_tweet({'id': id})
		neo4j.save_all()
		if not neo4j.check_tweet_exists(id):
			return False
	return True


def add_relationship(id_1, id_2):
	neo4j.add_wrote_relationship({"user_id": id_1, "tweet_id": id_2, "user_type": "Bot"})
	neo4j.save_all()
	return neo4j.check_writer_relationship({"user_id": id_1, "tweet_id": id_2, "user_type": "Bot"})


@pytest.fixture(scope='module')
def factory():
	return RequestFactory()


@pytest.fixture
def users_list(db):
	return mixer.cycle(20).blend(User, name="user1", screen_name="user2", protected=True)


@pytest.fixture
def user(db):
	return mixer.blend(User, id="1", user_id="1")


@pytest.fixture
def tweets(db):
	return mixer.cycle(20).blend(Tweet, user={"id": 1, "name": "user"}, tweet_id="1")


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
	path = reverse('twitter_users', kwargs={"protected": 'T'})
	request = factory.get(path)
	response = users.twitter_users(request, protected='T')
	assert is_response_successful_with_pagination(response, len(users_list))


@catch_exception
def test_successful_twitter_users_request_with_pagination(error_catcher, factory, users_list):
	path = reverse('twitter_users', kwargs={"protected": 'T', 'entries_per_page': 10, 'page': 1})
	request = factory.get(path)
	response = users.twitter_users(request, entries_per_page='10', page='1', protected='T')
	assert is_response_successful_with_pagination(response, 10)


@catch_exception
def test_empty_twitter_users_request(error_catcher, factory, db):
	path = reverse('twitter_users', kwargs={"protected": 'T'})
	request = factory.get(path)
	response = users.twitter_users(request, protected='T')
	assert is_response_empty_with_pagination(response)


@catch_exception
def test_unsuccessfully_twitter_users_request_with_pagination(error_catcher, factory, users_list):
	path = reverse('twitter_users', kwargs={"protected": 'T', 'entries_per_page': 0, 'page': 1})
	request = factory.get(path)
	response = users.twitter_users(request, entries_per_page='0', page='1', protected='T')
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
	assert add_bot_neo4j(["1"]) and add_tweet_neo4j(["1"]) and add_relationship("1", "1")
	path = reverse('twitter_user_tweets', kwargs={'user_id': 1})
	request = factory.get(path)
	response = users.twitter_user_tweets(request, user_id="1")
	assert is_response_successful_with_pagination(response, len(tweets))


@catch_exception
def test_successful_twitter_user_tweets_request_with_pagination(error_catcher, factory, tweets):
	assert add_bot_neo4j(["1"]) and add_tweet_neo4j(["1"]) and add_relationship("1", "1")
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
	assert add_bot_neo4j(["1"]) and add_tweet_neo4j(["1"]) and add_relationship("1", "1")
	path = reverse('twitter_user_tweets', kwargs={'user_id': 1, 'entries_per_page': 0, 'page': 1})
	request = factory.get(path)
	response = users.twitter_user_tweets(request, user_id="1", entries_per_page='0', page='1')
	assert is_response_unsuccessful(response)


@catch_exception
def test_successful_twitter_search_users_request(error_catcher, factory, users_list):
	path = reverse('twitter_search_users', kwargs={'keywords': "user", "protected": "T"})
	request = factory.get(path)
	response = users.twitter_search_users(request, keywords="user", protected='T')
	assert is_response_successful_with_pagination(response, len(users_list))


@catch_exception
def test_successful_twitter_search_users_request_with_pagination(error_catcher, factory, users_list):
	path = reverse('twitter_search_users',
	               kwargs={'keywords': "user", 'entries_per_page': 10, 'page': 1, "protected": "T"})
	request = factory.get(path)
	response = users.twitter_search_users(request, keywords="user", entries_per_page='10', page='1', protected='T')
	assert is_response_successful_with_pagination(response, 10)


@catch_exception
def test_empty_twitter_search_users_tweets_request(error_catcher, factory, db):
	path = reverse('twitter_search_users', kwargs={'keywords': "user", "protected": "T"})
	request = factory.get(path)
	response = users.twitter_search_users(request, keywords="user", protected='T')
	assert is_response_empty_with_pagination(response)


@catch_exception
def test_unsuccessfully_twitter_search_users_request_with_pagination(error_catcher, factory, users_list):
	path = reverse('twitter_search_users', kwargs={'keywords': "user", 'entries_per_page': 0,
	                                               'page': 1, "protected": "T"})
	request = factory.get(path)
	response = users.twitter_search_users(request, keywords="user", entries_per_page='0', page='1', protected='T')
	assert is_response_unsuccessful(response)
