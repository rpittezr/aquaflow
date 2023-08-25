from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.db import models
from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.controllers.serializers import UserProfileSerialize, UserHistorySerialize

from .models import UserProfile, ConsumedWater, UserHistory

from datetime import datetime
from itertools import groupby

def user_register(request):
    if request.method == 'POST':
        name = request.POST['name']
        weight = float(request.POST['weight'])
        user = User.objects.create_user(username=name)
        UserProfile.objects.create(user=user, weight=weight, name=name)
        return redirect('consume_register', user_id=user.id)
    return render(request, 'user_register.html')


def consume_register(request, user_id):
    user_profile = UserProfile.objects.get(user_id=user_id)
    selected_date_str = request.POST.get('selected_date')
    selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date() if selected_date_str else timezone.now().date()

    if request.method == 'POST':
        amount_ml = int(request.POST['amount_ml'])
        ConsumedWater.objects.create(user=user_profile, amount_ml=amount_ml, timestamp=selected_date)
        messages.success(request, 'Quantidade consumida!')

        return redirect('consume_register', user_id=user_id)  # Redirect to the same page (prevent resubmit)

    trackers = ConsumedWater.objects.filter(user=user_profile, timestamp__date=selected_date)
    total_ml = trackers.aggregate(models.Sum('amount_ml'))['amount_ml__sum'] or 0
    daily_goal = int(user_profile.weight * 35)
    remaining_ml = max(daily_goal - total_ml, 0)

    context = {
        'user_profile': user_profile,
        'trackers': trackers,
        'total_ml': total_ml,
        'daily_goal': daily_goal,
        'remaining_ml': remaining_ml,
        'selected_date': selected_date,
    }

    return render(request, 'consume_register.html', context)

