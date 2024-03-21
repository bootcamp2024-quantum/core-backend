from rest_framework import exceptions as rf_exceptions
from rest_framework import status, generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import User
from .serializers import UserSerializer, CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except rf_exceptions.ValidationError as e:
            msg = "\n".join([f"Field '{key}' may not be blank." for key in e.detail.keys()])
            return Response(data={"message": msg, "code": 400}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError as e:
            return Response(data={"message": ", ".join(e.args), "code": 500},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            _ = serializer.validated_data["code"]
            return Response(serializer.validated_data, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
