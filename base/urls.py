from django.urls import path
from . import views
from .controllers import users

urlpatterns = [
    path('users/<int:user_id>/history/', users.user_history, name='user_history'),
    path('users/', users.list_users, name="list_users"),
    path('users/register', users.user_register, name="user_register"),
    path('users/<int:user_id>/consume/', users.consume_register, name="consume_register"),
]