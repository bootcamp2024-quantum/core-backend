import json

from rest_framework import status
from rest_framework.test import APITestCase

from user.models import User


class GetUserApiViewTests(APITestCase):
    users_url = "/api/users/"
    user_request_data = {
        "username": "SomeUserName",
        "email": "someEmail@gmail.com",
        "password": "strongPassword",
        "avatar": None,
    }

    def test_get_user(self):
        user = User.objects.create(**self.user_request_data)
        response = self.client.get(self.users_url + str(user.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_body = response.content.decode("utf-8")
        parsed_response = json.loads(response_body)
        self.assertEqual(
            parsed_response["username"], self.user_request_data["username"]
        )
        self.assertEqual(parsed_response["email"], self.user_request_data["email"])
        self.assertEqual(parsed_response["avatar"], self.user_request_data["avatar"])

    def test_get_with_user(self):
        response = self.client.get(self.users_url + "5")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
