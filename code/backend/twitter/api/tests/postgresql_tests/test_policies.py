import pytest
from random import choice
from api.views import policies
from mixer.backend.django import mixer
from api.tests.utils import *
from api.models import Policy
from django.test import RequestFactory
from django.urls import reverse
from api.serializers import Policy as Policy_serializer
from api.enums import Policy as Enum_policy
from api import neo4j


@pytest.fixture(scope='module')
def factory():
    return RequestFactory()


@pytest.fixture
def policy(db):
    return mixer.blend(Policy, tags=["PSD", "PS"], bots=[1], id=1,
                       API_type=choice([x[0] for x in Enum_policy.api_types()]),
                       filter=choice([x[0] for x in Enum_policy.api_filter()]))


@pytest.fixture
def policy_twitter(db):
    return mixer.blend(Policy, tags=["PSD", "PS"], bots=[1], id=1,
                       API_type="Twitter", filter=choice([x[0] for x in Enum_policy.api_filter()]))


@pytest.fixture
def policy_instagram(db):
    return mixer.blend(Policy, tags=["PSD", "PS"], bots=[1], id=1,
                       API_type="Instagram", filter=choice([x[0] for x in Enum_policy.api_filter()]))


def add_bot_neo4j(bot_id=1):
    neo4j.add_bot({'id': bot_id, 'name': 'bot_test', 'username': 'bot_test_username'})
    return neo4j.check_bot_exists(bot_id)


@pytest.fixture(autouse=True)
def delete_neo4j_data():
    for bot_id in [1, 2]:
        neo4j.delete_bot(bot_id)
        if neo4j.check_bot_exists(bot_id):
            return False
    return True


@catch_exception
def test_successful_policies_request(error_catcher, factory, policy):
    path = reverse('policies')
    request = factory.get(path)
    response = policies.policies(request)
    assert is_response_successful(response)


@catch_exception
def test_unsuccessfully_policies_request(error_catcher, factory, db):
    path = reverse('policies')
    request = factory.get(path)
    response = policies.policies(request)
    assert is_response_empty(response)


@catch_exception
def test_successful_policy_request(error_catcher, factory, policy):
    path = reverse('policy', kwargs={'policy_id': 1})
    request = factory.get(path)
    response = policies.policy(request, policy_id=1)
    assert is_response_successful(response)


@catch_exception
def test_unsuccessfully_policy_request(error_catcher, factory, db):
    path = reverse('policy', kwargs={'policy_id': 1})
    request = factory.get(path)
    response = policies.policy(request, policy_id=1)
    assert is_response_unsuccessful(response)


@catch_exception
def test_successful_bot_policies_request(error_catcher, factory, policy):
    path = reverse('bot_policies', kwargs={'bot_id': 1})
    request = factory.get(path)
    response = policies.bot_policies(request, bot_id=1)
    assert is_response_successful(response)


@catch_exception
def test_unsuccessfully_bot_policies_request(error_catcher, factory, db):
    path = reverse('bot_policies', kwargs={'bot_id': 1})
    request = factory.get(path)
    response = policies.bot_policies(request, bot_id=1)
    assert is_response_empty(response)


@catch_exception
def test_successful_add_policy_request(error_catcher, factory, policy):
    assert add_bot_neo4j()
    path = reverse('add_policy')
    data = Policy_serializer(policy).data
    data.pop('id', None)
    data['tags'] = ["CDU"]
    data['name'] = 'politica2'
    request = factory.post(path, data, content_type='application/json')
    response = policies.add_policy(request)
    assert is_response_successful(response) and Policy.objects.filter().count() == 2


@catch_exception
def test_unsuccessfully_add_policy_with_duplicated_params_policies_request(error_catcher, factory, policy):
    assert add_bot_neo4j()
    path = reverse('add_policy')
    data = Policy_serializer(policy).data
    data.pop('id', None)
    request = factory.post(path, data, content_type='application/json')
    response = policies.add_policy(request)
    assert is_response_unsuccessful(response)


@catch_exception
def test_unsuccessfully_add_policy_with_invalid_bot_request(error_catcher, factory, policy):
    assert add_bot_neo4j(2)
    path = reverse('add_policy')
    data = Policy_serializer(policy).data
    data.pop('id', None)
    request = factory.post(path, data, content_type='application/json')
    response = policies.add_policy(request)
    assert is_response_unsuccessful(response)


@catch_exception
def test_unsuccessfully_add_policy_request(error_catcher, factory, db):
    path = reverse('add_policy')
    request = factory.post(path, content_type='application/json')
    response = policies.add_policy(request)
    assert is_response_unsuccessful(response)


@catch_exception
def test_successful_remove_policy_request(error_catcher, factory, policy):
    path = reverse('remove_policy', kwargs={'policy_id': 1})
    request = factory.delete(path)
    response = policies.remove_policy(request, policy_id=1)
    assert is_response_successful(response) and Policy.objects.filter().count() == 0


@catch_exception
def test_unsuccessfully_remove_policy_request(error_catcher, factory, db):
    path = reverse('remove_policy', kwargs={'policy_id': 1})
    request = factory.delete(path)
    response = policies.remove_policy(request, policy_id=1)
    assert is_response_unsuccessful(response)


@catch_exception
def test_successful_update_policy_request(error_catcher, factory, policy):
    path = reverse('update_policy', kwargs={'policy_id': 1})
    request = factory.put(path, {'name': 'bot_1'}, content_type='application/json')
    response = policies.update_policy(request, policy_id=1)
    assert is_response_successful(response) and Policy.objects.filter().count() == 1


@catch_exception
def test_unsuccessfully_update_policy_request(error_catcher, factory, db):
    path = reverse('update_policy', kwargs={'policy_id': 1})
    request = factory.put(path)
    response = policies.update_policy(request, policy_id=1)
    assert is_response_unsuccessful(response)

