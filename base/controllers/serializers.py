from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from base.models import UserProfile, ConsumedWater, UserHistory


class UserProfileSerialize(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('user', 'name', 'weight',)

class ConsumedWaterSerializer(ModelSerializer):
    amount_ml = serializers.IntegerField()
    class Meta:
        model = ConsumedWater
        fields = '__all__'

class UserHistorySerialize(serializers.Serializer):
    user_profile = UserProfileSerialize(source='user')
    daily_goal = serializers.IntegerField()
    total_consumed = serializers.ListField()
    grouped_trackers = serializers.DictField(child=serializers.ListField(child=ConsumedWaterSerializer()))
    goal_achievment = serializers.CharField(max_length=200)


