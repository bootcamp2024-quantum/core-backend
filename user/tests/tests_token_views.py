from rest_framework import status
from rest_framework.test import APITestCase
from user.models import User


class CustomTokenObtainPairViewTests(APITestCase):
    """Tests for obtaining a JWT token"""
    def setUp(self):
        """create test User instance"""
        User.objects.create_user(username='test_account', email='test@gmail.com', password='123')

    def test_successful_token_generation(self):
        """Test that the token is obtained by valid user"""
        url = '/token/'
        data = {'email': 'test@gmail.com', 'password': '123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_unexpected_fields_error(self):
        """request body have additional fields"""
        url = '/token/'
        data = {'email': 'test@gmail.com', 'password': '123', 'trash_data': '123456789'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_blank_field_email_error(self):
        """email field is blank."""
        url = '/token/'
        data = {'email': '', 'password': '123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['code'], 400)
        self.assertEqual(len(response.data['message']), 1)

    def test_blank_field_password_error(self):
        """password field is blank"""
        url = '/token/'
        data = {'email': 'test@gmail.com', 'password': ''}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['code'], 400)
        self.assertEqual(len(response.data['message']), 1)

    def test_blank_fields_error(self):
        """email and password fields are blank."""
        url = '/token/'
        data = {'email': '', 'password': ''}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['code'], 400)
        self.assertEqual(len(response.data['message']), 2)

    def test_not_existed_user_error(self):
        """invalid email and password fields."""
        url = '/token/'
        data = {'email': 'no_existing@gmail.com', 'password': '3213213213'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['code'], 400)
        self.assertEqual(response.data['message'], "Invalid credentials")
