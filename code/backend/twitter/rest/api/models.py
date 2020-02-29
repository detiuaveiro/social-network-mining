from django.db import models


class Tweet(models.Model):
	id = models.IntegerField(primary_key=True)
	user = models.TextField()
	is_quote_status = models.BooleanField()
	quoted_status_id = models.IntegerField(null=True, blank=True)
	in_reply_to_screen_name = models.TextField(null=True, blank=True)
	in_reply_to_user_id = models.IntegerField(null=True, blank=True)
	in_reply_to_status_id = models.IntegerField(null=True, blank=True)

	class Meta:
		managed = True
		db_table = "tweets"

