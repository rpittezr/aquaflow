from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    weight = models.FloatField()

    class Meta:
        app_label = 'base'

class ConsumedWater(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount_ml = models.PositiveIntegerField()
    timestamp = models.DateTimeField()