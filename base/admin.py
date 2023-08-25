from django.contrib import admin

# Register your models here.

from .models import UserProfile, ConsumedWater

admin.site.register(UserProfile)
admin.site.register(ConsumedWater)