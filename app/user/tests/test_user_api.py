from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class TestCreateUserAPI(TestCase):

    def setUp(self):
        self.api_client = APIClient()

    def test_create_user_with_valid_data(self):
        """ Test create user with valid data. """

        payload = {"email": "test_user1@recepi.org", "password": "Test123",
                   "name": "Test name"}
        res = self.api_client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_exists(self):
        """ Test fails when create user that already exists. """

        payload = {"email": "test_user@recepi.org", "password": "Test123"}
        create_user(**payload)
        res = self.api_client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_short_password(self):
        """ Test verify user password must be more then 5 characters. """

        payload = {"email": "test_user@recepi.org", "password": "pw",
                   "name": "Test name"}
        res = self.api_client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload["email"]
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """ Test that a token is created for the user. """

        payload = {"email": "test_user2@recepi.org", "password": "Test1234"}
        create_user(**payload)
        res = self.api_client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """ Test that token is not created if invalid credentials are given.
        """

        payload = {"email": "test_user@recepi.org", "password": "testpass"}
        create_user(**payload)
        payload['password'] = "wrong"
        res = self.api_client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_no_user(self):
        """ Test that token is not created if user doesn't exists. """

        payload = {"email": "test_user@recepi.org", "password": "testpass"}
        res = self.api_client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)
