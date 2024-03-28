from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from rest_framework.exceptions import AuthenticationFailed as RF_AuthenticationFailed
from rest_framework import status


class CustomAuthenticationFailed(RF_AuthenticationFailed):
    pass


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)

        if header is None:
            self.raise_custom_error(
                "Authentication credentials were not provided.",
                status.HTTP_401_UNAUTHORIZED
            )

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            self.raise_custom_error(
                "Authentication credentials were invalid.",
                status.HTTP_401_UNAUTHORIZED
            )

        try:
            validated_token = self.get_validated_token(raw_token)
            user = self.get_user(validated_token)
        except InvalidToken as e:
            self.raise_custom_error(
                str(e.detail["detail"]),
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except AuthenticationFailed as e:
            self.raise_custom_error(
                str(e.detail["detail"]),
                status.HTTP_401_UNAUTHORIZED
            )
        else:
            return user, validated_token

    def raise_custom_error(self, message="Server error.", code=500):
        raise CustomAuthenticationFailed({"message": message, "code": code})
