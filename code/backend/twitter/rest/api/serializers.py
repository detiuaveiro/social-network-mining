from rest_framework import serializers


class Tweet(serializers.Serializer):
	id = serializers.IntegerField(required=True)
	user = serializers.CharField(required=True)
	is_quote_status = serializers.BooleanField(required=True)
	quoted_status_id = serializers.IntegerField()
	in_reply_to_screen_name = serializers.CharField()
	in_reply_to_user_id = serializers.IntegerField()
	in_reply_to_status_id = serializers.IntegerField()
