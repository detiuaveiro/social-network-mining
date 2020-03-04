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
    id = models.IntegerField(primary_key=True)
    API_type = models.TextField()
    filter = models.TextField()
    name = models.TextField()
    tags = ArrayField(models.TextField())
    bots = ArrayField(models.IntegerField())
    active = models.BooleanField(default=False)
