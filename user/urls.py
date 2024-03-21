from django.urls import path

from .views import UserCreateView, UserDeleteUpdateRetrieveView

app_name = 'user'

urlpatterns = [
    path('', UserCreateView.as_view(), name='user-create'),
    path('<int:pk>', UserDeleteUpdateRetrieveView.as_view(), name='user-delete'),
]
