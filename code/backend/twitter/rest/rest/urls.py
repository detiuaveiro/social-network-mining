"""rest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from api import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path("twitter/users", views.twitter_users, name="twitter_users"),
    path("twitter/users/stats", views.twitter_users_stats, name="twitter_users_stats"),
    url(r"^twitter/users/(?P<id>[0-9]+)", views.twitter_user, name="twitter_user"),
    url(r"^twitter/users/(?P<id>[0-9]+)/tweets", views.twitter_user_tweets, name="twitter_user_tweets"),
    url(r"^twitter/users/(?P<id>[0-9]+)/followers", views.twitter_user_followers, name="twitter_user_followers"),
    url(r"^twitter/users/(?P<id>[0-9]+)/following", views.twitter_user_following, name="twitter_user_following"),
    url(r"^twitter/users/(?P<id>[0-9]+)/stats", views.twitter_user_stats, name="twitter_user_stats"),
    url("twitter/users/export", views.twitter_users_export, name="twitter_users_export"),

    path("twitter/network", views.twitter_network, name="twitter_network"),
    path("twitter/network/export", views.twitter_network_export, name="twitter_network_export"),

    path("twitter/create", views.twitter_create, name="twitter_create"),
    path("twitter/stats", views.twitter_stats, name="twitter_stats"),

    path("twitter/bots", views.twitter_bots, name="twitter_bots"),
    url(r"^twitter/bots/(?P<id>[0-9]+)", views.twitter_bot, name="twitter_bot"),
    url(r"^twitter/bots/(?P<id>[0-9]+)/logs", views.twitter_bot_logs, name="twitter_bot_logs"),
    url(r"^twitter/bots/(?P<id>[0-9]+)/messages", views.twitter_bot_messages, name="twitter_bot_messages"),

    path("twitter/tweets", views.twitter_tweets, name="twitter_tweets"),
    path("twitter/tweets/export", views.twitter_tweets_export, name="twitter_tweets_export"),
    path("twitter/tweets/stats", views.twitter_tweets_stats, name="twitter_tweets_stats"),
    url(r"^twitter/tweets/(?P<id>[0-9]+)", views.twitter_tweet, name="twitter_tweet"),
    url(r"^twitter/tweets/(?P<id>[0-9]+)/stats", views.twitter_tweet_stats, name="twitter_tweet_stats"),
    url(r"^twitter/tweets/(?P<id>[0-9]+)/replies", views.twitter_tweet_replies, name="twitter_tweet_replies"),

    path("policies", views.policies, name="policies"),
    url(r"^policies/(?P<id>[0-9]+)", views.policy, name="policy"),
    url(r"^policies/bots/(?P<id>[0-9]+)", views.bot_policies, name="bot_policies"),
    path("policies/add", views.add_policy, name="add_policy"),
    url(r"^policies/remove/(?P<id>[0-9]+)", views.remove_policy, name="remove_policy"),
    url(r"^policies/update", views.update_policy, name="update_policy"),
    url(r"^policies/instagram", views.instagram_policies, name="instagram_policies"),
    path("policies/twitter", views.twitter_policies, name="twitter_policies"),
]
