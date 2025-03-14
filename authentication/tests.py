from rest_framework import status
from rest_framework.test import APITestCase


class UserTests(APITestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "email": "testuser@gmail.com",
            "password": "userpass",
            "role": "user",
        }
        self.admin_data = {
            "username": "adminuser",
            "email": "admin@gmail.com",
            "password": "adminpass",
            "role": "admin",
        }
        self.register_url = "/api/register/"
        self.login_url = "/api/login/"

    def test_register_user(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["username"], "testuser")

    def test_register_with_missing_fields(self):
        response = self.client.post(self.register_url, {"username": "user_1"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_successful(self):
        self.client.post(self.register_url, self.user_data)
        response = self.client.post(self.login_url, {"username": "testuser", "password": "userpass"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("refresh", response.json())
        self.assertIn("access", response.json())

    def test_login_invalid_credentials(self):
        self.client.post(self.register_url, self.user_data)
        response = self.client.post(self.login_url, {"username": "testuser", "password": "wrongpassword"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()["detail"], "No active account found with the given credentials")

    def test_login_unregistered_user(self):
        response = self.client.post(self.login_url, {"username": "fakeuser", "password": "somepassword"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()["detail"], "No active account found with the given credentials")
