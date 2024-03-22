from django.urls import path

from .views import CustomTokenObtainPairView, UserCreateView

app_name = "user"


urlpatterns = [
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("", UserCreateView.as_view(), name="user-create"),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), CSA-55
]
