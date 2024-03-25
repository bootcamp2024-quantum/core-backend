from django.urls import path
from user.views import (UserCreateAPIView, UserPasswordUpdateAPIView,
                        UserRetrieveUpdateDestroyAPIView)

app_name = "user"

urlpatterns = [
    path("", UserCreateAPIView.as_view(), name="user-create"),
    path("<int:pk>/", UserRetrieveUpdateDestroyAPIView.as_view(), name="user-retrieve-update-destroy"),
    path("<int:pk>/password/", UserPasswordUpdateAPIView.as_view(), name="user-password-update")
]
