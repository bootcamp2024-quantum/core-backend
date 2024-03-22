from django.urls import path

from .views import CustomTokenObtainPairView, CustomTokenRefreshView, UserCreateView

app_name = "user"

urlpatterns = [
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("", UserCreateView.as_view(), name="user-create"),
]
