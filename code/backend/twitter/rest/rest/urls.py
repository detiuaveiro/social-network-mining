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

from api.views import users, bots, tweets, policies, network


urlpatterns = [
    path('admin/', admin.site.urls),

    path("twitter/users", users.twitter_users, name="twitter_users"),
    path("twitter/users/stats", users.twitter_users_stats, name="twitter_users_stats"),
    url(r"^twitter/users/(?P<id>[0-9]+)", users.twitter_user, name="twitter_user"),
    url(r"^twitter/users/(?P<id>[0-9]+)/tweets", users.twitter_user_tweets, name="twitter_user_tweets"),
    url(r"^twitter/users/(?P<id>[0-9]+)/followers", users.twitter_user_followers, name="twitter_user_followers"),
    url(r"^twitter/users/(?P<id>[0-9]+)/following", users.twitter_user_following, name="twitter_user_following"),
    url(r"^twitter/users/(?P<id>[0-9]+)/stats", users.twitter_user_stats, name="twitter_user_stats"),
    url("twitter/users/export", users.twitter_users_export, name="twitter_users_export"),

    path("twitter/network", network.twitter_network, name="twitter_network"),
    path("twitter/network/export", network.twitter_network_export, name="twitter_network_export"),

    path("twitter/create", bots.twitter_create, name="twitter_create"),
    path("twitter/stats", bots.twitter_stats, name="twitter_stats"),
    path("twitter/bots", bots.twitter_bots, name="twitter_bots"),
    url(r"^twitter/bots/(?P<id>[0-9]+)", bots.twitter_bot, name="twitter_bot"),
    url(r"^twitter/bots/(?P<id>[0-9]+)/logs", bots.twitter_bot_logs, name="twitter_bot_logs"),
    url(r"^twitter/bots/(?P<id>[0-9]+)/messages", bots.twitter_bot_messages, name="twitter_bot_messages"),

    url(r"^twitter/tweets(/limit=(?P<limit>[0-9]+))?", tweets.twitter_tweets, name="twitter_tweets"),
    path("twitter/tweets/export", tweets.twitter_tweets_export, name="twitter_tweets_export"),
    path("twitter/tweets/stats", tweets.twitter_tweets_stats, name="twitter_tweets_stats"),
    url(r"^twitter/tweets/(?P<id>[0-9]+)", tweets.twitter_tweet, name="twitter_tweet"),
    url(r"^twitter/tweets/(?P<id>[0-9]+)/stats", tweets.twitter_tweet_stats, name="twitter_tweet_stats"),
    url(r"^twitter/tweets/(?P<id>[0-9]+)/replies", tweets.twitter_tweet_replies, name="twitter_tweet_replies"),

    path("policies", policies.policies, name="policies"),
    url(r"^policies/(?P<id>[0-9]+)", policies.policy, name="policy"),
    url(r"^policies/bots/(?P<id>[0-9]+)", policies.bot_policies, name="bot_policies"),
    path("policies/add", policies.add_policy, name="add_policy"),
    url(r"^policies/remove/(?P<id>[0-9]+)", policies.remove_policy, name="remove_policy"),
    url(r"^policies/update", policies.update_policy, name="update_policy"),
    url(r"^policies/instagram", policies.instagram_policies, name="instagram_policies"),
    path("policies/twitter", policies.twitter_policies, name="twitter_policies"),
]
