from rest_framework import exceptions as rf_exceptions
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import (CreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
from user.models import User
from user.serializers import (CustomTokenObtainPairSerializer,
                              CustomTokenRefreshSerializer,
                              UserCreateSerializer,
                              UserPasswordUpdateSerializer,
                              UserRetrieveUpdateDestroySerializer)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except rf_exceptions.ValidationError as e:
            msg = "\n".join(
                [f"Field '{key}' may not be blank." for key in e.detail.keys()]
            )
            return Response(
                data={"message": msg, "code": 400}, status=status.HTTP_400_BAD_REQUEST
            )
        except TokenError as e:
            return Response(
                data={"message": ", ".join(e.args), "code": 500},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        try:
            _ = serializer.validated_data["code"]
            return Response(
                serializer.validated_data, status=status.HTTP_400_BAD_REQUEST
            )
        except KeyError:
            return Response(data=serializer.validated_data, status=status.HTTP_200_OK)


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        try:
            if serializer.validated_data["access"]:
                return Response(data=serializer.validated_data, status=status.HTTP_200_OK)
        except KeyError:
            if serializer.validated_data["code"] == status.HTTP_400_BAD_REQUEST:
                status_code = status.HTTP_400_BAD_REQUEST
            else:
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            return Response(data=serializer.validated_data, status=status_code)


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                data={"message": "Bad request.", "code": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserRetrieveUpdateDestroySerializer


class UserPasswordUpdateAPIView(UpdateAPIView):
    serializer_class = UserPasswordUpdateSerializer

    def put(self, request, *args, **kwargs):

        try:
            user = self.get_user_object(kwargs.get("pk"))
        except NotFound as error:
            return Response(data={"error": str(error)}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            return self.update_password(user, serializer.validated_data)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_user_object(user_id: int):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound(f"User object with id = {user_id} does not exist.")

    @staticmethod
    def update_password(user, validated_data):
        current_password = validated_data.get("current_password")
        new_password = validated_data.get("new_password")

        if user.check_password(current_password):
            user.set_password(new_password)
            user.save()
            return Response(
                data={"message": "Password updated successfully."},
                status=status.HTTP_200_OK,
            )
        else:
            Response(
                data={"message": "Current password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )
