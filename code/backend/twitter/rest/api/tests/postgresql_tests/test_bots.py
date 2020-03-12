import pytest
from django.test import RequestFactory
from django.urls import reverse
from api.models import UserStats
from api.views import bots
from mixer.backend.django import mixer
from api.tests.utils import *


@pytest.fixture(scope='module')
def factory():
    return RequestFactory()


@pytest.fixture
def user_stats(db):
    return mixer.blend(UserStats)


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
