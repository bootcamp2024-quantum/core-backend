import json

from rest_framework import status
from rest_framework.test import APITestCase

from user.models import User


class GetUserApiViewTests(APITestCase):

    def setUp(self):
        self.users_url = "/api/users/"
        self.user_request_data = {
            "name": "SomeUserName",
            "email": "someEmail@gmail.com",
            "password": "strongPassword",
            "avatar": None,
        }
        self.user = User.objects.create(username=self.user_request_data["name"],
                                        email=self.user_request_data["email"],
                                        password=self.user_request_data["password"],
                                        avatar=self.user_request_data["avatar"])
        self.client.force_authenticate(self.user)

    def test_get_user(self):
        response = self.client.get(self.users_url + str(self.user.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_body = response.content.decode("utf-8")
        parsed_response = json.loads(response_body)
        self.assertEqual(
            parsed_response["name"], self.user_request_data["name"]
        )
        self.assertEqual(parsed_response["email"], self.user_request_data["email"])
        self.assertEqual(parsed_response["avatar"], self.user_request_data["avatar"])

    def test_get_unexisting_user(self):
        response = self.client.get(self.users_url + "5" + "/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
