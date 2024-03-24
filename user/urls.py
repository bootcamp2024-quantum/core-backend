from django.urls import path

from .views import (CustomTokenObtainPairView, CustomTokenRefreshView,
                    UserCreateView, UserDeleteUpdateRetrieveView)

app_name = "user"

urlpatterns = [
    path("", UserCreateView.as_view(), name="user-create"),
    path("<int:pk>", UserDeleteUpdateRetrieveView.as_view(), name="user-delete"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh")
]
