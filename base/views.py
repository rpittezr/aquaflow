from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.db import models

from .models import UserProfile, ConsumedWater

from datetime import datetime
from itertools import groupby

def user_register(request):
    if request.method == 'POST':
        name = request.POST['name']
        weight = float(request.POST['weight'])
        user = User.objects.create_user(username=name)
        UserProfile.objects.create(user=user, weight=weight)
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

def user_history(request, user_id):
    user_profile = UserProfile.objects.get(user_id=user_id)
    
    trackers = ConsumedWater.objects.filter(user=user_profile).order_by('timestamp')

    # Group tracker (ordered by date)
    grouped_trackers = {}
    for date, group in groupby(trackers, key=lambda x: x.timestamp.date()):
        grouped_trackers[date] = list(group)
    
    # Calculate the goal
    daily_goal = int(user_profile.weight * 35)

    # Calculate consumed water per day
    total_consumed = []
    for date, trackers in grouped_trackers.items():
        total_amount = sum(tracker.amount_ml for tracker in trackers)
        total_consumed.append((date, total_amount))

    context = {
        'user_profile': user_profile,
        'grouped_trackers': grouped_trackers,
        'daily_goal': daily_goal,
        'total_consumed': total_consumed,  # Pass the list of tuples to the template
    }

    return render(request, 'user_history.html', context)

