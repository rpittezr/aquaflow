from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default="default_user")
    weight = models.FloatField()

    def __str__(self):
        return self.name

class ConsumedWater(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount_ml = models.PositiveIntegerField()
    timestamp = models.DateTimeField()


class UserHistory():
    def __init__(self, **kwargs):
        self.user = kwargs['user']
        self.grouped_trackers = kwargs['grouped_trackers']
        self.daily_goal = kwargs['daily_goal']
        self.total_consumed = kwargs['total_consumed']
        self.goal_achievment = kwargs['goal_achievment']
