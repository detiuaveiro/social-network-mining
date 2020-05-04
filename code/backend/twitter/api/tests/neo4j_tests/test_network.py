from django.test import RequestFactory
from django.urls import reverse
from api.views import network
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
		if not neo4j.check_bot_exists(id):
			return False
	return True


def add_relationship(id_1, id_2):
	neo4j.add_follow_relationship({"id_1": id_1, "id_2": id_2, "type_1": "Bot", "type_2": "Bot"})
	return neo4j.check_follow_exists({"id_1": id_1, "id_2": id_2, "type_1": "Bot", "type_2": "Bot"})


@catch_exception
def test_empty_twitter_sub_network_request(error_catcher, factory):
	path = reverse('twitter_sub_network')
	request = factory.get(path)
	response = network.twitter_sub_network(request)
	assert is_response_empty(response)


@catch_exception
def test_successful_twitter_network_request(error_catcher, factory):
	assert add_bot_neo4j(["1", "2", "3"]) and add_relationship("2", "1") and add_relationship("3", "1")
	path = reverse('twitter_network')
	request = factory.get(path)
	response = network.twitter_network(request)
	assert is_response_successful(response)


@catch_exception
def test_empty_twitter_network_request(error_catcher, factory):
	path = reverse('twitter_network')
	request = factory.get(path)
	response = network.twitter_network(request)
	assert is_response_empty(response)
