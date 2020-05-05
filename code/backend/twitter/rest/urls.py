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
from rest_framework_swagger.views import get_swagger_view

from api.views import users, bots, tweets, policies, network, graphics

schema_view = get_swagger_view(title='TwitterBots API')

urlpatterns = [
	url('documentation/', schema_view),

	path('admin/', admin.site.urls),

	# Users
	url(r"^twitter/users/count/$", users.twitter_users_count, name='twitter_users_count'),

	url(r"^twitter/users/$", users.twitter_users, name="twitter_users"),
	url(r"^twitter/users/(?P<entries_per_page>[0-9]+)/(?P<page>[0-9]+)/$", users.twitter_users, name="twitter_users"),

	url(r"^twitter/users/stats/$", users.twitter_users_stats, name="twitter_users_stats"),
	url(r"^twitter/users/stats/(?P<entries_per_page>[0-9]+)/(?P<page>[0-9]+)/$", users.twitter_users_stats,
		name="twitter_users_stats"),

	url(r"^twitter/users/(?P<user_id>[0-9]+)/$", users.twitter_user, name="twitter_user"),

	url(r"^twitter/users/(?P<user_id>[0-9]+)/tweets/$", users.twitter_user_tweets, name="twitter_user_tweets"),
	url(r"^twitter/users/(?P<user_id>[0-9]+)/tweets/(?P<entries_per_page>[0-9]+)/(?P<page>[0-9]+)/$",
		users.twitter_user_tweets, name="twitter_user_tweets"),

	url(r"^twitter/users/(?P<user_id>[0-9]+)/followers/$", users.twitter_user_followers, name="twitter_user_followers"),
	url(r"^twitter/users/(?P<user_id>[0-9]+)/followers/(?P<entries_per_page>[0-9]+)/(?P<page>[0-9]+)/$",
		users.twitter_user_followers, name="twitter_user_followers"),

	url(r"^twitter/users/(?P<user_id>[0-9]+)/following/$", users.twitter_user_following, name="twitter_user_following"),
	url(r"^twitter/users/(?P<user_id>[0-9]+)/following/(?P<entries_per_page>[0-9]+)/(?P<page>[0-9]+)/$",
		users.twitter_user_following, name="twitter_user_following"),

	url(r"^twitter/users/(?P<user_id>[0-9]+)/stats/$", users.twitter_user_stats, name="twitter_user_stats"),
	url(r"^twitter/users/(?P<user_id>[0-9]+)/stats/(?P<entries_per_page>[0-9]+)/(?P<page>[0-9]+)/$",
		users.twitter_user_stats, name="twitter_user_stats"),

	url(r"^twitter/users/search/(?P<keywords>[\w\s()]+)/$", users.twitter_search_users, name="twitter_search_users"),
	url(r"^twitter/users/search/(?P<keywords>[\w\s()]+)/(?P<entries_per_page>[0-9]+)/(?P<page>[0-9]+)/$",
		users.twitter_search_users, name="twitter_search_users"),

	url(r"^twitter/users/(?P<user_id>[0-9]+)/stats/grouped/(?P<group_type>(?:year)|(?:month)|(?:day))/$",
		users.twitter_user_stats_grouped, name="twitter_user_stats_grouped"),
	url(r"twitter/users/(?P<id>[0-9]+)/type/$", users.twitter_users_type, name="users.twitter_users_type"),

	# Network
	path("twitter/network", network.twitter_network, name="twitter_network"),

	path("twitter/sub_network", network.twitter_sub_network, name="twitter_sub_network"),

	# Bots
	path("twitter/bots", bots.twitter_bots, name="twitter_bots"),

	url(r"^twitter/bots/(?P<bot_id>[0-9]+)/$", bots.twitter_bot, name="twitter_bot"),

	url(r"^twitter/bots/(?P<bot_id>[0-9]+)/logs/$", bots.twitter_bot_logs, name="twitter_bot_logs"),
	url(r"^twitter/bots/(?P<bot_id>[0-9]+)/logs/(?P<entries_per_page>[0-9]+)/(?P<page>[0-9]+)/$", bots.twitter_bot_logs,
		name="twitter_bot_logs"),

	url(r"^twitter/bots/(?P<bot_id>[0-9]+)/messages/$", bots.twitter_bot_messages, name="twitter_bot_messages"),

	# Tweets
	path(r"twitter/tweets/all", tweets.twitter_tweets, name="twitter_tweets"),
	url(r"^twitter/tweets/all/(?P<entries_per_page>[0-9]+)/(?P<page>[0-9]+)/$", tweets.twitter_tweets,
		name="twitter_tweets"),

	url(r"^twitter/tweets/stats/$", tweets.twitter_tweets_stats, name="twitter_tweets_stats"),
	url(r"^twitter/tweets/stats/(?P<entries_per_page>[0-9]+)/(?P<page>[0-9]+)/$",
		tweets.twitter_tweets_stats, name="twitter_tweets_stats"),

	url(r"^twitter/tweets/(?P<tweet_id>[0-9]+)/$", tweets.twitter_tweet, name="twitter_tweet"),

	url(r"^twitter/tweets/(?P<tweet_id>[0-9]+)/stats/$", tweets.twitter_tweet_stats, name="twitter_tweet_stats"),
	url(r"^twitter/tweets/(?P<tweet_id>[0-9]+)/stats/(?P<entries_per_page>[0-9]+)/(?P<page>[0-9]+)/$",
		tweets.twitter_tweet_stats, name="twitter_tweet_stats"),

	url(r"^twitter/tweets/(?P<tweet_id>[0-9]+)/replies/$", tweets.twitter_tweet_replies, name="twitter_tweet_replies"),

	# Policies
	url(r"^policies/$", policies.policies, name="policies"),
	url(r"^policies/(?P<entries_per_page>[0-9]+)/(?P<page>[0-9]+)/$", policies.policies, name="policies"),

	url(r"^policies/(?P<policy_id>[0-9]+)/$", policies.policy, name="policy"),

	url(r"^policies/bots/(?P<bot_id>[0-9]+)/$", policies.bot_policies, name="bot_policies"),
	url(r"^policies/bots/(?P<bot_id>[0-9]+)/(?P<entries_per_page>[0-9]+)/(?P<page>[0-9]+)/$", policies.bot_policies,
		name="bot_policies"),

	path("policies/add", policies.add_policy, name="add_policy"),

	url(r"^policies/remove/(?P<policy_id>[0-9]+)/$", policies.remove_policy, name="remove_policy"),

	url(r"^policies/update/(?P<policy_id>[0-9]+)/$", policies.update_policy, name="update_policy"),

	url(r"^policies/number", policies.get_number_policies, name="number_policies"),

	# Graphics
	path('entities/counter', graphics.entities_counter, name="entities_counter"),

	url(r'^graphs/latest_tweets/(?P<counter>[0-9]+)$', graphics.latest_tweets, name="latest_tweets"),
	url(r'^graphs/latest_tweets/(?P<counter>[0-9]+)/(?P<entries_per_page>[0-9]+)/(?P<page>[0-9]+)/$',
		graphics.latest_tweets, name="latest_tweets"),

	path('graphs/latest_activities/daily/', graphics.latest_activities, name="latest_activities"),
	url(r'^graphs/latest_activities/daily/(?P<entries_per_page>[0-9]+)/(?P<page>[0-9]+)/$',
		graphics.latest_activities, name="latest_activities"),
]
