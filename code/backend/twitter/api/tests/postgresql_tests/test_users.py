from django.test import RequestFactory
from django.urls import reverse
from api.models import UserStats
from api.views import users
from mixer.backend.django import mixer
from api.tests.utils import *
from datetime import datetime, timedelta


@pytest.fixture(scope='module')
def factory():
	return RequestFactory()


@pytest.fixture
def users_stats(db):
	return mixer.cycle(20).blend(UserStats)


@pytest.fixture
def user_stats(db):
	return mixer.cycle(20).blend(UserStats, user_id=1, protected=True, timestamp=datetime(2020, 2, 2))


@catch_exception
def test_successful_twitter_users_stats_request(error_catcher, factory, users_stats):
	path = reverse('twitter_users_stats', kwargs={"protected": "T"})
	request = factory.get(path)
	response = users.twitter_users_stats(request, protected="T")
	assert is_response_successful_with_pagination(response)


@catch_exception
def test_successful_twitter_users_stats_request_with_pagination(error_catcher, factory, users_stats):
	path = reverse('twitter_users_stats', kwargs={"entries_per_page": 10, "page": 1, "protected": "T"})
	request = factory.get(path)
	response = users.twitter_users_stats(request, entries_per_page=10, page=1, protected="T")
	assert is_response_successful_with_pagination(response)


@catch_exception
def test_empty_twitter_users_stats_request(error_catcher, factory, db):
	path = reverse('twitter_users_stats', kwargs={"protected": "T"})
	request = factory.get(path)
	response = users.twitter_users_stats(request, protected="T")
	assert is_response_empty_with_pagination(response)


@catch_exception
def test_unsuccessfully_twitter_users_stats_request_with_pagination(error_catcher, factory, users_stats):
	path = reverse('twitter_users_stats', kwargs={"entries_per_page": 0, "page": 1, "protected": "T"})
	request = factory.get(path)
	response = users.twitter_users_stats(request, entries_per_page=0, page=1, protected="T")
	assert is_response_unsuccessful(response)


@catch_exception
def test_successful_twitter_user_stats_request(error_catcher, factory, user_stats):
	path = reverse('twitter_user_stats', kwargs={'user_id': 1})
	request = factory.get(path)
	response = users.twitter_user_stats(request, user_id=1)
	assert is_response_successful_with_pagination(response)


@catch_exception
def test_successful_twitter_user_stats_request_with_pagination(error_catcher, factory, user_stats):
	path = reverse('twitter_user_stats', kwargs={'user_id': 1, 'entries_per_page': 10, 'page': 1})
	request = factory.get(path)
	response = users.twitter_user_stats(request, user_id=1, entries_per_page=10, page=1)
	assert is_response_successful_with_pagination(response)


@catch_exception
def test_empty_twitter_user_stats_request(error_catcher, factory, db):
	path = reverse('twitter_user_stats', kwargs={'user_id': 1})
	request = factory.get(path)
	response = users.twitter_user_stats(request, user_id=1)
	assert is_response_empty_with_pagination(response)


@catch_exception
def test_unsuccessfully_twitter_user_stats_request_with_pagination(error_catcher, factory, user_stats):
	path = reverse('twitter_user_stats', kwargs={'user_id': 1, 'entries_per_page': 0, 'page': 1})
	request = factory.get(path)
	response = users.twitter_user_stats(request, user_id=1, entries_per_page=0, page=1)
	assert is_response_unsuccessful(response)


@catch_exception
def test_successful_twitter_user_stats_grouped_request(error_catcher, factory, user_stats):
	path = reverse('twitter_user_stats_grouped', kwargs={'user_id': 1, 'group_type': 'year'})
	request = factory.get(path)
	response = users.twitter_user_stats_grouped(request, user_id=1, group_type='year')
	assert is_response_successful(response)


@catch_exception
def test_empty_twitter_user_stats_grouped_request(error_catcher, factory, db):
	path = reverse('twitter_user_stats_grouped', kwargs={'user_id': 1, 'group_type': 'year'})
	request = factory.get(path)
	response = users.twitter_user_stats_grouped(request, user_id=1, group_type='year')
	assert is_response_unsuccessful(response)
