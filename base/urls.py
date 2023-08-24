from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_register, name='user_register'),
    path('consume/<int:user_id>/', views.consume_register, name='consume_register'),
    path('history/<int:user_id>/', views.user_history),
]