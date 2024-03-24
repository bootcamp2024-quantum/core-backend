from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from user.models import User


class CreateUserApiViewTests(APITestCase):
    users_url = "/api/users/"
    user_request_data = {
        "username": "SomeUserName",
        "email": "someEmail@gmail.com",
        "password": "strongPassword",
        "repeat_password": "strongPassword",
        "avatar": None,
    }

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username="admin",
            email="admin@gmail.com",
            password="strongAdmin",
            avatar=None,
        )
        self.client.force_authenticate(self.user)

    def test_create_new_user(self):
        response = self.client.post(
            self.users_url, self.user_request_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="SomeUserName").exists())

    def test_create_new_user_without_password(self):
        response = self.client.post(
            self.users_url, self.user_request_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(username="test_user").exists())

    def test_create_new_user_with_invalid_email(self):
        self.user_request_data["email"] = "someEmail@.com"
        response = self.client.post(
            self.users_url, self.user_request_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(username="test_user").exists())
