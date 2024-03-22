from django.core.exceptions import ObjectDoesNotExist
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from rest_framework import generics, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.serializers import CharField
from rest_framework.views import APIView

from user.models import User
from user.serializers import ChangePasswordSerializer, UserPUTSerializer, UserSerializer


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


@extend_schema(tags=["Users"])
class UserUpdatePasswordView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        request=ChangePasswordSerializer,
        examples=[
            OpenApiExample(
                "Update User password with the specified parameters",
                description="Update User password with the specified parameters",
                request_only=True,
                value={
                    "current_password": "strongPassword",
                    "new_password": "strong1Password",
                },
            ),
        ],
        responses={
            "200": OpenApiResponse(
                response=inline_serializer(
                    name="Password updated successfully.",
                    fields={
                        "message": CharField(),
                    },
                ),
            ),
            "400": OpenApiResponse(
                description="Validation error or incorrect current password.",
                response=inline_serializer(
                    name="Validation error or incorrect current password.",
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
        tags=["Users"],
    )
    def put(self, request, *args, **kwargs):

        try:
            user = User.objects.get(id=kwargs.get("pk"))
        except ObjectDoesNotExist:
            return Response(
                {"error": f"User object with id = {kwargs.get('pk')} does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            if user.check_password(request.data["current_password"]):
                user.set_password(serializer.validated_data["new_password"])
                user.save()
                return Response(
                    {"message": "Password updated successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Current password doesn't correct"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
