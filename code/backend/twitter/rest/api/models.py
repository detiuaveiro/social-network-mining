from django.db import models
from djongo import models as djongo_models


class Tweet(djongo_models.Model):
	id = djongo_models.IntegerField(primary_key=True, db_column="_id")
	tweet_id = djongo_models.IntegerField(db_column="id")
	user = djongo_models.TextField()
	is_quote_status = djongo_models.BooleanField()
	quoted_status_id = djongo_models.IntegerField(null=True, blank=True)
	in_reply_to_screen_name = djongo_models.TextField(null=True, blank=True)
	in_reply_to_user_id = djongo_models.IntegerField(null=True, blank=True)
	in_reply_to_status_id = djongo_models.IntegerField(null=True, blank=True)

	class Meta:
		managed = True
		db_table = "tweets"

