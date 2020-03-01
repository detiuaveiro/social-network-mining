from rest_framework import serializers
from api.enums import Policy as enum_policy


class Tweet(serializers.Serializer):
    tweet_id = serializers.IntegerField(required=True)
    user = serializers.CharField(required=True)
    is_quote_status = serializers.BooleanField(required=True)
    quoted_status_id = serializers.IntegerField()
    in_reply_to_screen_name = serializers.CharField()
    in_reply_to_user_id = serializers.IntegerField()
    in_reply_to_status_id = serializers.IntegerField()




class Policy(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    API_type = serializers.ChoiceField(choices=enum_policy.api_types())
    filter = serializers.ChoiceField(choices=enum_policy.api_filter())
    name = serializers.CharField()
    tags = serializers.ListField(child=serializers.CharField())
    bots = serializers.ListField(child=serializers.IntegerField(validators=[]))
    active = serializers.BooleanField(required=False)






