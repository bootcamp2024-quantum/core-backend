from rest_framework import status
from rest_framework.test import APITestCase

from user.models import User


class CustomTokenObtainPairViewTests(APITestCase):
    """Tests for obtaining a JWT token"""

    def setUp(self):
        """create test User instance"""
        User.objects.create_user(
            username="test_account", email="test@gmail.com", password="123"
        )

    def test_successful_token_generation(self):
        """Test that the token is obtained by valid user"""
        url = "/api/token/"
        data = {"email": "test@gmail.com", "password": "123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_unexpected_fields_error(self):
        """request body have additional fields"""
        url = "/api/token/"
        data = {"email": "test@gmail.com", "password": "123", "trash_data": "123456789"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_blank_field_email_error(self):
        """email field is blank."""
        url = "/api/token/"
        data = {"email": "", "password": "123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["code"], 400)
        self.assertEqual(response.data["message"], "Field 'email' may not be blank.")

    def test_blank_field_password_error(self):
        """password field is blank"""
        url = "/api/token/"
        data = {"email": "test@gmail.com", "password": ""}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["code"], 400)
        self.assertEqual(response.data["message"], "Field 'password' may not be blank.")

    def test_blank_fields_error(self):
        """email and password fields are blank."""
        url = "/api/token/"
        data = {"email": "", "password": ""}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["code"], 400)
        self.assertEqual(len(response.data["message"].split("\n")), 2)
        self.assertEqual(
            response.data["message"].split("\n"),
            ["Field 'email' may not be blank.", "Field 'password' may not be blank."],
        )

    def test_not_existed_user_error(self):
        """invalid email and password fields."""
        url = "/api/token/"
        data = {"email": "no_existing@gmail.com", "password": "3213213213"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["code"], 400)
        self.assertEqual(response.data["message"], "Invalid credentials")

    def test_http_500_internal_server_error(self):
        """internal server error handling test"""
        pass


class TokenRefreshViewTests(APITestCase):

    def setUp(self):
        email = "test@gmail.com"
        password = "123"
        username = "testUser"
        User.objects.create_user(
            email=email,
            password=password,
            username=username,
        )
        self.token_pair = self.client.post(
            "/api/token/", {"email": email, "password": password}, format="json"
        ).data

    def test_refresh_success(self):
        """refresh success."""
        response = self.client.post(
            "/api/token/refresh/",
            {"refresh": self.token_pair["refresh"]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_refresh_blank_field(self):
        """refresh field is blank."""
        response = self.client.post(
            "/api/token/refresh/", {"refresh": ""}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Field 'refresh' may not be blank.")
        self.assertEqual(response.data["code"], 400)

    def test_refresh_error(self):
        """invalid token provided."""
        response = self.client.post(
            "/api/token/refresh/",
            {
                "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90"
                "eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxMTEzMjE3OCwiaWF0I"
                "joxNzExMDQ1Nzc4LCJqdGkiOiIyYTUwNjgxOTM2ODA0MzgwOW"
                "U0MTMwN1241VmZmY4NiIsInVzZXJfaWQiOjF9.ZquTX19QaR2"
                "1451u6SFI0u066Xq-LcJ67rJTyDMk-1E"
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data["message"], "Token is invalid or expired")
        self.assertEqual(response.data["code"], status.HTTP_500_INTERNAL_SERVER_ERROR)
