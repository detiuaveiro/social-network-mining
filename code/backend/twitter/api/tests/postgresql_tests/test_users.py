import pytest
from django.test import RequestFactory
from django.urls import reverse
from api.models import UserStats
from api.views import users
from mixer.backend.django import mixer
from api.tests.utils import *
from api import neo4j


@pytest.fixture(scope='module')
def factory():
    return RequestFactory()


@pytest.fixture
def users_stats(db):
    return mixer.cycle(5).blend(UserStats)


@pytest.fixture
def user_stats(db):
    return mixer.blend(UserStats, id=1, user_id=1)


@catch_exception
def test_successful_twitter_users_stats_request(error_catcher, factory, users_stats):
    path = reverse('twitter_users_stats')
    request = factory.get(path)
    response = users.twitter_users_stats(request)
    assert is_response_successful(response)


@catch_exception
def test_unsuccessfully_twitter_users_stats_request(error_catcher, factory, db):
    path = reverse('twitter_users_stats')
    request = factory.get(path)
    response = users.twitter_users_stats(request)
    assert is_response_empty(response)


@catch_exception
def test_successful_twitter_user_stats_request(error_catcher, factory, user_stats):
    path = reverse('twitter_user_stats', kwargs={'id': 1})
    request = factory.get(path)
    response = users.twitter_user_stats(request, id=1)
    assert is_response_successful(response)


@catch_exception
def test_unsuccessfully_twitter_user_stats_request(error_catcher, factory, db):
    path = reverse('twitter_user_stats', kwargs={'id': 1})
    request = factory.get(path)
    response = users.twitter_user_stats(request, id=1)
    assert is_response_empty(response)
