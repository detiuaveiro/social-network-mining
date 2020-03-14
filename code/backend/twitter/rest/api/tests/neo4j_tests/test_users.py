import pytest
from django.test import RequestFactory
from django.urls import reverse
from api.views import users
from mixer.backend.django import mixer
from api.tests.utils import *
from api import neo4j


@pytest.fixture(scope='module')
def factory():
    return RequestFactory()


@pytest.fixture(autouse=True)
def delete_neo4j_data():
    for id in [1, 2]:
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
    neo4j.add_relationship({"id_1": id_1, "id_2": id_2, "type_1": "Bot", "type_2": "Bot"})
    return neo4j.check_relationship_exists({"id_1": id_1, "id_2": id_2, "type_1": "Bot", "type_2": "Bot"})


def test_successful_twitter_user_followers_request(factory):
    assert add_bot_neo4j([1, 2]) and add_relationship(2, 1)
    path = reverse('twitter_user_followers', kwargs={'id': 1})
    request = factory.get(path)
    response = users.twitter_user_followers(request, id=1)
    assert is_response_successful(response)


def test_unsuccessfully_twitter_user_followers_request(factory):
    path = reverse('twitter_user_followers', kwargs={'id': 1})
    request = factory.get(path)
    response = users.twitter_user_followers(request, id=1)
    assert is_response_unsuccessful(response)


def test_successful_twitter_user_following_request(factory):
    assert add_bot_neo4j([1, 2]) and add_relationship(1, 2)
    path = reverse('twitter_user_following', kwargs={'id': 1})
    request = factory.get(path)
    response = users.twitter_user_following(request, id=1)
    assert is_response_successful(response)


def test_unsuccessfully_twitter_user_following_request(factory):
    path = reverse('twitter_user_following', kwargs={'id': 1})
    request = factory.get(path)
    response = users.twitter_user_following(request, id=1)
    assert is_response_unsuccessful(response)
