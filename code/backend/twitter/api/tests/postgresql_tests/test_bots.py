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


@catch_exception
def test_successful_twitter_bot_logs_request(error_catcher, factory, logs):
	entries_per_page = 1
	page = 1
	path = reverse('twitter_bot_logs', kwargs={'id': 1, 'entries_per_page': entries_per_page, 'page': page})
	request = factory.get(path)
	response = bots.twitter_bot_logs(request, id=1, entries_per_page=str(entries_per_page), page=str(page))
	assert is_response_successful(response)


@catch_exception
def test_unsuccessfully_twitter_bot_logs_request(error_catcher, factory, db):
	entries_per_page = 1
	page = 1
	path = reverse('twitter_bot_logs', kwargs={'id': 1, 'entries_per_page': entries_per_page, 'page': page})
	request = factory.get(path)
	response = bots.twitter_bot_logs(request, id=1, entries_per_page=str(entries_per_page), page=str(page))

	assert response.status_code == 200 and len(response.data['error_messages']) == 0 and \
	       len(response.data['success_messages']) > 0 and response.data['data']['entries'] == []
