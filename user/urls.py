from django.urls import path

from user.views import (
    UserCreateView,
    UserDeleteUpdateRetrieveView,
    UserUpdatePasswordView,
)

app_name = "user"

urlpatterns = [
    path("", UserCreateView.as_view(), name="user-create"),
    path(
        "<int:pk>",
        UserDeleteUpdateRetrieveView.as_view(),
        name="user-delete_update_retrieve",
    ),
    path(
        "<int:pk>/password",
        UserUpdatePasswordView.as_view(),
        name="user-update_password",
    ),
]
