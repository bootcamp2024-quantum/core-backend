from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from user.models import User


class DeleteUserApiViewTests(APITestCase):
    users_url = "/api/users/"

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

    def test_delete_user(self):
        response = self.client.delete(self.users_url + str(self.test_user.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(username="TestSomeUserName").exists())

    def test_delete_unexcisted_id_user(self):
        response = self.client.delete(self.users_url + str(self.test_user.id + 1))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
