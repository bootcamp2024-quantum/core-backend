import json

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from user.models import User


# todo add tests for avatar field
class PutUserApiViewTests(APITestCase):
    users_url = "/api/users/"
    user_request_data = {
        "username": "SomeUserName",
        "email": "someEmail@gmail.com",
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
        self.test_user = User.objects.create(
            username="TestSomeUserName",
            email="TestEmail@gmail.com",
            password="strongPassword",
            avatar=None,
        )

    def test_update_user(self):

        url = self.users_url + str(self.test_user.id)

        response = self.client.put(url, self.user_request_data, format="json")
        response_body = response.content.decode("utf-8")
        parsed_response = json.loads(response_body)
        user = User.objects.get(id=self.test_user.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(parsed_response["username"], user.username)
        self.assertEqual(parsed_response["email"], user.email)
