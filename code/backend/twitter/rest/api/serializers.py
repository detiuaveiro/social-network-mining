from rest_framework import serializers
from api.enums import Policy as enum_policy


class Tweet(serializers.Serializer):
    tweet_id = serializers.IntegerField()
    user = serializers.CharField()
    is_quote_status = serializers.BooleanField()
    quoted_status_id = serializers.IntegerField(required=False)
    in_reply_to_screen_name = serializers.CharField(required=False)
    in_reply_to_user_id = serializers.IntegerField(required=False)
    in_reply_to_status_id = serializers.IntegerField(required=False)


class Policy(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    API_type = serializers.ChoiceField(choices=enum_policy.api_types())
    filter = serializers.ChoiceField(choices=enum_policy.api_filter())
    name = serializers.CharField()
    tags = serializers.ListField(child=serializers.CharField())
    bots = serializers.ListField(child=serializers.IntegerField(validators=[]))
    active = serializers.BooleanField(required=False)
