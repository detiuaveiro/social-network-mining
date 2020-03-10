import pytest
import random
from django.test import TestCase
from api.models import UserStats
from mixer.backend.django import mixer

@pytest.mark.django_db
class TestBots(TestCase):
    databases = "__all__"

    @classmethod
    def setUpClass(cls):
        super(TestBots,cls).setUpClass()
        UserStats.objects.using("postgres").create(user_id=1, following=1, followers=1)

    #@pytest.fixture
    #def user_stats(db):
    #    return


    def test_twitter_stats(self):
        assert True
