import pytest
from django.test import RequestFactory
from django.urls import reverse
from api.models import UserStats, Log
from api.views import bots
from mixer.backend.django import mixer
from api.tests.utils import *


@pytest.fixture(scope='module')
def factory():
    return RequestFactory()


@pytest.fixture
def user_stats(db):
    return mixer.blend(UserStats)


@pytest.fixture
def logs(db):
    return mixer.cycle(20).blend(Log, id_bot=1)


def test_successful_twitter_stats_request(factory, user_stats):
    path = reverse('twitter_stats')
    request = factory.get(path)
    response = bots.twitter_stats(request)
    assert is_response_successful(response)


def test_unsuccessfully_twitter_stats_request(factory, db):
    path = reverse('twitter_stats')
    request = factory.get(path)
    response = bots.twitter_stats(request)
    assert is_response_empty(response)


def test_successful_twitter_bot_logs_request(factory, logs):
    limit = 1
    path = reverse('twitter_bot_logs', kwargs={'id': 1, 'limit': limit})
    request = factory.get(path)
    response = bots.twitter_bot_logs(request, id=1, limit=str(limit))
    print(response.data['data'])
    assert is_response_successful(response) and len(response.data['data']) == limit


def test_unsuccessfully_twitter_bot_logs_request(factory, db):
    limit = 1
    path = reverse('twitter_bot_logs', kwargs={'id': 1, 'limit': limit})
    request = factory.get(path)
    response = bots.twitter_bot_logs(request, id=1, limit=str(limit))
    assert is_response_empty(response)
