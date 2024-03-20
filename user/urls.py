from django.urls import path

from .views import UserCreateView

app_name = 'user'

urlpatterns = [
    path('user/', UserCreateView.as_view(), name='user-create'),
]
