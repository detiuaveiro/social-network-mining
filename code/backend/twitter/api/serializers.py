from rest_framework import serializers
from api.enums import Policy as enum_policy


class User(serializers.Serializer):
	user_id = serializers.CharField()
	description = serializers.CharField()
	location = serializers.CharField()
	name = serializers.CharField()
	screen_name = serializers.CharField()
	followers_count = serializers.IntegerField()
	friends_count = serializers.IntegerField()
	profile_image_url_https = serializers.CharField()
	protected = serializers.BooleanField()


class UserStats(serializers.Serializer):
	user_id = serializers.CharField()
	timestamp = serializers.DateTimeField()
	followers = serializers.IntegerField()
	following = serializers.IntegerField()
	protected = serializers.BooleanField()


class Variant(serializers.Serializer):
	bitrate = serializers.IntegerField(required=False)
	content_type = serializers.CharField()
	url = serializers.URLField()


class VideoInfo(serializers.Serializer):
	variants = serializers.ListField(child=Variant(), allow_empty=True)


class Media(serializers.Serializer):
	id = serializers.IntegerField()
	type = serializers.CharField()
	media_url_https = serializers.URLField()
	video_info = VideoInfo(required=False)


class ExtendedEntities(serializers.Serializer):
	media = serializers.ListField(child=Media(), allow_empty=True)


class Tweet(serializers.Serializer):
	tweet_id = serializers.CharField(required=True)
	user = serializers.DictField()
	is_quote_status = serializers.BooleanField(required=True)
	created_at = serializers.DateTimeField(required=True)
	quoted_status_id = serializers.IntegerField()
	in_reply_to_screen_name = serializers.CharField()
	in_reply_to_user_id = serializers.CharField()
	in_reply_to_status_id = serializers.CharField()
	in_reply_to_status_id_str = serializers.CharField(required=False)
	extended_entities = ExtendedEntities(required=False)
	text = serializers.CharField()
	full_text = serializers.CharField()
	retweet_count = serializers.IntegerField()
	favorite_count = serializers.IntegerField()


class TweetStats(serializers.Serializer):
	tweet_id = serializers.IntegerField()
	user_id = serializers.IntegerField()
	likes = serializers.IntegerField()
	retweets = serializers.IntegerField()
	timestamp = serializers.DateTimeField()


class Policy(serializers.Serializer):
	id = serializers.IntegerField(required=False)
	API_type = serializers.ChoiceField(choices=enum_policy.api_types(), default="Twitter")
	filter = serializers.ChoiceField(choices=enum_policy.api_filter(), default="Keywords")
	name = serializers.CharField()
	tags = serializers.ListField(child=serializers.CharField(), allow_empty=False)
	bots = serializers.ListField(child=serializers.CharField())
	active = serializers.BooleanField(required=False)


class Log(serializers.Serializer):
	id_bot = serializers.CharField()
	timestamp = serializers.DateTimeField()
	action = serializers.CharField()
	target_id = serializers.CharField()


class Url(serializers.Serializer):
	url = serializers.EmailField()
	expanded_url = serializers.EmailField()
	display_url = serializers.CharField()
	indices = serializers.ListField(child=serializers.IntegerField())


class Message_entities(serializers.Serializer):
	hashtags = serializers.ListField(child=serializers.CharField(), allow_empty=True)
	symbols = serializers.ListField(child=serializers.CharField(), allow_empty=True)
	user_mentions = serializers.ListField(child=serializers.CharField(), allow_empty=True)
	urls = serializers.ListField(child=Url(), allow_empty=True)


class Message(serializers.Serializer):
	id = serializers.IntegerField(required=False)
	created_at = serializers.CharField()
	recipient_id = serializers.IntegerField()
	sender_id = serializers.IntegerField()
	text = serializers.CharField()
	entities = Message_entities(required=False)
	bot_id = serializers.CharField()


class Notification(serializers.Serializer):
	email = serializers.EmailField(required=True)
	status = serializers.BooleanField(default=True)
