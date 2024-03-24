from drf_spectacular.utils import (OpenApiExample, OpenApiResponse,
                                   extend_schema, inline_serializer)
from rest_framework import exceptions as rf_exceptions
from rest_framework import generics, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import CharField
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from . import serializers
from .models import User
from .serializers import UserPUTSerializer, UserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer

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
            return Response(serializer.validated_data, status=status.HTTP_200_OK)


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = serializers.CustomTokenRefreshSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        try:
            if serializer.validated_data["access"]:
                return Response(serializer.validated_data, status=status.HTTP_200_OK)
        except KeyError:
            if serializer.validated_data["code"] == status.HTTP_400_BAD_REQUEST:
                status_code = status.HTTP_400_BAD_REQUEST
            else:
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            return Response(data=serializer.validated_data, status=status_code)


@extend_schema(tags=["Users"])
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        request=UserSerializer,
        examples=[
            OpenApiExample(
                "Create User with the specified parameters",
                description="Create User with the specified parameters",
                request_only=True,
                value={
                    "username": "SomeUserName",
                    "email": "someEmail@gmail.com",
                    "password": "strongPassword",
                    "repeat_password": "strongPassword",
                    "avatar": None,
                },
            ),
        ],
        responses={
            "201": OpenApiResponse(
                response=UserSerializer,
            ),
            "400": OpenApiResponse(
                description="",
                response=inline_serializer(
                    name="Validation error.",
                    fields={
                        "error": bool,
                        "message": CharField(),
                    },
                ),
            ),
        },
    )
    @action(detail=False, methods=["post"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@extend_schema(tags=["Users"])
class UserDeleteUpdateRetrieveView(
    generics.RetrieveDestroyAPIView, mixins.UpdateModelMixin
):
    queryset = User.objects.all()
    serializer_class = UserPUTSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        request=UserPUTSerializer,
        examples=[
            OpenApiExample(
                "Get User by ID",
                description="Get User by ID",
                request_only=True,
                value={
                    "username": "SomeUserName",
                    "email": "someEmail@gmail.com",
                    "avatar": None,
                },
            ),
        ],
        responses={
            "200": OpenApiResponse(
                response=UserPUTSerializer,
            ),
            "404": OpenApiResponse(
                description="User object with ID {id} does not exist.",
                response=inline_serializer(
                    name="User object with ID {id} does not exist.",
                    fields={
                        "error": bool,
                        "message": CharField(),
                    },
                ),
            ),
        },
    )
    @action(detail=False, methods=["get"])
    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        request=UserPUTSerializer,
        examples=[
            OpenApiExample(
                "Update User with the specified parameters",
                description="Update User with the specified parameters",
                request_only=True,
                value={
                    "username": "SomeUserName",
                    "email": "someEmail@gmail.com",
                    "avatar": None,
                },
            ),
        ],
        responses={
            "200": OpenApiResponse(
                response=UserPUTSerializer,
            ),
            "400": OpenApiResponse(
                description="Validation error for User object with ID.",
                response=inline_serializer(
                    name="Validation error for User object with ID.",
                    fields={
                        "error": bool,
                        "message": CharField(),
                    },
                ),
            ),
            "404": OpenApiResponse(
                description="User object with ID does not exist.",
                response=inline_serializer(
                    name="User object with ID does not exist.",
                    fields={
                        "error": bool,
                        "message": CharField(),
                    },
                ),
            ),
        },
    )
    def put(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
