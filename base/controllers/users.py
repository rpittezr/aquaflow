from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from base.models import UserProfile, ConsumedWater, UserHistory
from django.contrib.auth.models import User
from datetime import datetime
from itertools import groupby

from base.controllers.serializers import UserProfileSerialize, UserHistorySerialize

@api_view(['POST'])
def user_register(request):
    try:
        name = request.POST['name']
        weight = float(request.POST['weight'])
        user = User.objects.create_user(username=name)
        UserProfile.objects.create(user=user, weight=weight, name=name)
        return Response({'message': "Cadastrado com sucesso!" })
    except Exception as e:
        return Response({'message': "Houve um problema no cadastro", 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def consume_register(request, user_id):
    try:
        user_profile = UserProfile.objects.get(user_id=user_id)
        selected_date_str = request.POST.get('selected_date')
        selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date() if selected_date_str else timezone.now().date()

        amount_ml = int(request.POST['amount_ml'])
        ConsumedWater.objects.create(user=user_profile, amount_ml=amount_ml, timestamp=selected_date)

        return Response({'message': "Quantidade consumida!" })

    except Exception as e:
        return Response({'message': "Houve um problema no cadastro", 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_users(request):
    users = UserProfile.objects.all()
    serializer = UserProfileSerialize(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def list_histories(request):
    histories = ConsumedWater.objects.all()
    serializer = UserHistorySerialize(histories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def user_history(request, user_id):
    user_profile = UserProfile.objects.get(user_id=user_id)
    
    trackers = ConsumedWater.objects.filter(user=user_profile).order_by('timestamp')

    # Group tracker (ordered by date)
    grouped_trackers = {}
    for date, group in groupby(trackers, key=lambda x: x.timestamp.date()):
        grouped_trackers[str(date)] = list(group)
    
    # Calculate the goal
    daily_goal = int(user_profile.weight * 35)

    # Calculate consumed water per day
    total_consumed = []
    for date, trackers in grouped_trackers.items():
        total_amount = sum(tracker.amount_ml for tracker in trackers)
        total_consumed.append((date, total_amount))

    goal_achievment = ""
    if total_amount >= daily_goal:
        goal_achievment = "Sim"
    else:
        goal_achievment = "Não"

    user_history = UserHistory(user=user_profile, grouped_trackers=grouped_trackers,
    daily_goal=daily_goal, total_consumed=total_consumed, goal_achievment=goal_achievment)

    serializer = UserHistorySerialize(user_history, many=False)
    print(serializer.data)
    return Response(serializer.data)

