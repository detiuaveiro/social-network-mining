from django.utils.timezone import now
from djongo import models as djongo_models
from django.contrib.postgres.fields import ArrayField
from django.db import models


class User(djongo_models.Model):
	id = djongo_models.IntegerField(primary_key=True, db_column="_id")
	user_id = djongo_models.IntegerField(db_column="id")
	description = djongo_models.TextField()
	location = djongo_models.TextField()
	name = djongo_models.TextField()
	screen_name = djongo_models.TextField()
	followers_count = djongo_models.IntegerField()
	friends_count = djongo_models.IntegerField()
	profile_image_url_https = djongo_models.TextField()

	class Meta:
		managed = True
		db_table = "users"


class UserStats(models.Model):
	user_id = models.BigIntegerField()
	timestamp = models.DateTimeField(default=now, primary_key=True)
	followers = models.IntegerField()
	following = models.IntegerField()

	class Meta:
		managed = True
		db_table = "users"


class Variant(djongo_models.Model):
	bitrate = djongo_models.BigIntegerField(blank=True, null=True)
	content_type = djongo_models.TextField()
	url = djongo_models.URLField()


class VideoInfo(djongo_models.Model):
	variants = djongo_models.ListField(Variant, null=True, blank=True)


class Media(djongo_models.Model):
	id = djongo_models.BigIntegerField(primary_key=True)
	type = djongo_models.TextField()
	media_url_https = djongo_models.URLField()
	video_info = djongo_models.EmbeddedField(VideoInfo, blank=True, null=True)


class ExtendedEntities(djongo_models.Model):
	media = djongo_models.ListField(Media, null=True, blank=True)


class Tweet(djongo_models.Model):
	id = djongo_models.BigIntegerField(primary_key=True, db_column="_id")
	tweet_id = djongo_models.BigIntegerField(db_column="id")
	tweet_id_str = djongo_models.TextField(db_column="id_str")
	user = djongo_models.BigIntegerField()
	is_quote_status = djongo_models.BooleanField()
	created_at = djongo_models.DateTimeField()
	quoted_status_id = djongo_models.BigIntegerField(null=True, blank=True)
	in_reply_to_screen_name = djongo_models.TextField(null=True, blank=True)
	in_reply_to_user_id = djongo_models.BigIntegerField(null=True, blank=True)
	in_reply_to_status_id = djongo_models.BigIntegerField(null=True, blank=True)
	extended_entities = djongo_models.EmbeddedField(ExtendedEntities, blank=True, null=True)
	text = djongo_models.TextField()
	retweet_count = djongo_models.BigIntegerField()
	favorite_count = djongo_models.BigIntegerField()

	class Meta:
		managed = True
		db_table = "tweets"


class TweetStats(models.Model):
	tweet_id = models.BigIntegerField()
	user_id = models.IntegerField()
	likes = models.IntegerField()
	retweets = models.IntegerField()
	timestamp = models.DateTimeField(primary_key=True)

	class Meta:
		managed = True
		db_table = "tweets"


class Policy(models.Model):
	id = models.IntegerField(primary_key=True, db_column="id_policy")
	API_type = models.TextField(db_column="api_type")
	filter = models.TextField()
	name = models.TextField(unique=True)  # alter table policies add constraint unique_name unique(name);
	tags = ArrayField(models.TextField(), db_column="params")
	bots = ArrayField(models.DecimalField(max_digits=128, decimal_places=0))
	active = models.BooleanField(default=False)

	class Meta:
		managed = True
		db_table = "policies"
		unique_together = ["API_type", "filter", "tags"]


class Log(models.Model):
	id_bot = models.IntegerField(primary_key=True)
	timestamp = models.DateTimeField()
	action = models.TextField()
	target_id = models.BigIntegerField()

	class Meta:
		managed = True
		db_table = 'logs'


class Url(djongo_models.Model):
	url = djongo_models.EmailField()
	expanded_url = djongo_models.EmailField()
	display_url = djongo_models.TextField()
	indices = djongo_models.ListField(djongo_models.IntegerField())


class Message_entities(djongo_models.Model):
	hashtags = djongo_models.ListField(djongo_models.TextField())
	symbols = djongo_models.ListField(djongo_models.TextField())
	user_mentions = djongo_models.ListField(djongo_models.TextField())
	urls = djongo_models.ListField(Url)


class Message(djongo_models.Model):
	id = djongo_models.BigIntegerField(primary_key=True, db_column="_id")
	created_at = djongo_models.TextField()
	recipient_id = djongo_models.BigIntegerField()
	sender_id = djongo_models.BigIntegerField()
	text = djongo_models.TextField()
	entities = djongo_models.EmbeddedField(Message_entities, blank=True, null=True)
	bot_id = djongo_models.TextField()

	class Meta:
		managed = True
		db_table = "messages"
