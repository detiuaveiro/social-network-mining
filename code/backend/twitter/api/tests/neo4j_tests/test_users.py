from django.test import RequestFactory
from django.urls import reverse
from api.views import users
from api.tests.utils import *
from api import neo4j


@pytest.fixture(scope='module')
def factory():
	return RequestFactory()


@pytest.fixture(autouse=True)
def delete_neo4j_data():
	for id in ["1", "2", "3"]:
		neo4j.delete_bot(id)
		if neo4j.check_bot_exists(id):
			return False
	return True


def add_bot_neo4j(list_id):
	for id in list_id:
		neo4j.add_bot({'id': id, 'name': 'bot_test', 'username': 'bot_test_username'})
		neo4j.save_all()
		if not neo4j.check_bot_exists(id):
			return False
	return True


def add_relationship(id_1, id_2):
	neo4j.add_follow_relationship({"id_1": id_1, "id_2": id_2, "type_1": "Bot", "type_2": "Bot"})
	neo4j.save_all()
	return neo4j.check_follow_exists({"id_1": id_1, "id_2": id_2, "type_1": "Bot", "type_2": "Bot"})


@catch_exception
def test_successful_twitter_user_followers_request(error_catcher, factory):
	assert add_bot_neo4j(["1", "2", "3"]) and add_relationship("2", "1") and add_relationship("3", "1")
	path = reverse('twitter_user_followers', kwargs={'user_id': "1"})
	request = factory.get(path)
	response = users.twitter_user_followers(request, user_id="1")
	print(response.data)
	assert is_response_successful_with_pagination(response, 2)


@catch_exception
def test_successful_twitter_user_followers_request_with_pagination(error_catcher, factory):
	assert add_bot_neo4j(["1", "2", "3"]) and add_relationship("2", "1") and add_relationship("3", "1")
	path = reverse('twitter_user_followers', kwargs={'user_id': "1", "entries_per_page": 1, 'page': 1})
	request = factory.get(path)
	response = users.twitter_user_followers(request, user_id="1", entries_per_page=1, page=1)
	assert is_response_successful_with_pagination(response, 1)


@catch_exception
def test_empty_twitter_user_followers_request(error_catcher, factory):
	path = reverse('twitter_user_followers', kwargs={'user_id': "1"})
	request = factory.get(path)
	response = users.twitter_user_followers(request, user_id="1")
	assert is_response_empty_with_pagination(response)


@catch_exception
def test_unsuccessfully_twitter_user_followers_request_with_with_pagination(error_catcher, factory):
	assert add_bot_neo4j(["1", "2", "3"]) and add_relationship("2", "1") and add_relationship("3", "1")
	path = reverse('twitter_user_followers', kwargs={'user_id': "1", "entries_per_page": 0, 'page': 1})
	request = factory.get(path)
	response = users.twitter_user_followers(request, user_id="1", entries_per_page=0, page=1)
	assert is_response_unsuccessful(response)


@catch_exception
def test_successful_twitter_user_following_request(error_catcher, factory):
	assert add_bot_neo4j(["1", "2", "3"]) and add_relationship("1", "2") and add_relationship("1", "3")
	path = reverse('twitter_user_following', kwargs={'user_id': "1"})
	request = factory.get(path)
	response = users.twitter_user_following(request, user_id="1")
	assert is_response_successful_with_pagination(response, 2)


@catch_exception
def test_successful_twitter_user_following_request_with_with_pagination(error_catcher, factory):
	assert add_bot_neo4j(["1", "2", "3"]) and add_relationship("1", "2") and add_relationship("1", "3")
	path = reverse('twitter_user_following', kwargs={'user_id': "1", "entries_per_page": 1, 'page': 1})
	request = factory.get(path)
	response = users.twitter_user_following(request, user_id="1", entries_per_page=1, page=1)
	assert is_response_successful_with_pagination(response, 1)


@catch_exception
def test_empty_twitter_user_following_request(error_catcher, factory):
	path = reverse('twitter_user_following', kwargs={'user_id': "1"})
	request = factory.get(path)
	response = users.twitter_user_following(request, user_id="1")
	assert is_response_empty_with_pagination(response)


@catch_exception
def test_unsuccessfully_twitter_user_following_request_with_pagination(error_catcher, factory):
	assert add_bot_neo4j(["1", "2", "3"]) and add_relationship("1", "2") and add_relationship("1", "3")
	path = reverse('twitter_user_following', kwargs={'user_id': "1", "entries_per_page": 0, 'page': 1})
	request = factory.get(path)
	response = users.twitter_user_following(request, user_id="1", entries_per_page=0, page=1)
	assert is_response_unsuccessful(response)
