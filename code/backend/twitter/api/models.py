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
    user_id = models.BigIntegerField(primary_key=True)
    timestamp = models.DateTimeField(default=now)
    followers = models.IntegerField()
    following = models.IntegerField()

    class Meta:
        managed = True
        db_table = "users"


class Tweet(djongo_models.Model):
    id = djongo_models.IntegerField(primary_key=True, db_column="_id")
    tweet_id = djongo_models.IntegerField(db_column="id")
    user = djongo_models.IntegerField()
    is_quote_status = djongo_models.BooleanField()
    quoted_status_id = djongo_models.IntegerField(null=True, blank=True)
    in_reply_to_screen_name = djongo_models.TextField(null=True, blank=True)
    in_reply_to_user_id = djongo_models.IntegerField(null=True, blank=True)
    in_reply_to_status_id = djongo_models.IntegerField(null=True, blank=True)

    class Meta:
        managed = True
        db_table = "tweets"


class TweetStats(models.Model):
    tweet_id = models.BigIntegerField(primary_key=True)
    user_id = models.IntegerField()
    likes = models.IntegerField()
    retweets = models.IntegerField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = True
        db_table = "tweets"


class Policy(models.Model):
    id = models.IntegerField(primary_key=True, db_column="id_policy")
    API_type = models.TextField(db_column="api_type")
    filter = models.TextField()
    name = models.TextField(unique=True)  # alter table policies add constraint unique_name unique(name);
    tags = ArrayField(models.TextField(), db_column="params")
    bots = ArrayField(models.BigIntegerField())
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
