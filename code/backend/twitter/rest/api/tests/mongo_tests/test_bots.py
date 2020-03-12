import pytest
from django.test import RequestFactory
from django.urls import reverse
from api.models import User, Message
from api.views import bots
from mixer.backend.django import mixer
from api.tests.utils import *
from api import neo4j


@pytest.fixture(scope='module')
def factory():
    return RequestFactory()


@pytest.fixture
def user(db):
    return mixer.blend(User, id=1, user_id=1)


def add_bot_neo4j():
    neo4j.add_bot({'id': 1, 'name': 'bot_test', 'username': 'bot_test_username'})
    return neo4j.check_bot_exists(1)


@pytest.fixture
def message(db):
    return mixer.blend(Message, entitites=None)


def test_successful_twitter_bots_request(factory, user):
    assert add_bot_neo4j()
    path = reverse('twitter_bots')
    request = factory.get(path)
    response = bots.twitter_bots(request)
    assert is_response_successful(response)


def test_unsuccessfully_twitter_bots_request(factory, db):
    path = reverse('twitter_bots')
    request = factory.get(path)
    response = bots.twitter_bots(request)
    assert is_response_empty(response)


def test_successful_twitter_bot_request(factory):
    assert add_bot_neo4j()
    path = reverse('twitter_bot', kwargs={'id': 1})
    request = factory.get(path)
    response = bots.twitter_bot(request, id=1)
    assert is_response_successful(response)


def test_unsuccessfully_twitter_bot_request(factory):
    path = reverse('twitter_bot', kwargs={'id': 1})
    request = factory.get(path)
    response = bots.twitter_bot(request, id=1)
    assert is_response_empty(response)


#def test_successful_twitter_bot_messages_request(factory, message):
#    path = reverse('twitter_bot_messages', kwargs={'id': '1'})
#    request = factory.get(path)
#    response = bots.twitter_bot_messages(request, id='1')
#    assert is_response_successful(response)
#
#
#def test_unsuccessfully_twitter_bot_messages_request(factory, db):
#    path = reverse('twitter_bot_messages', kwargs={'id': '1'})
#    request = factory.get(path)
#    response = bots.twitter_bot_messages(request, id='1')
#    assert is_response_unsuccessful(response)
