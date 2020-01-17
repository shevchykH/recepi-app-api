from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user():
    """ Create sample user. """

    return get_user_model().objects.create_user(
        email="sample_user@recipe.org",
        password='testpass123'
    )


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """ Test creating a new user with email is successful. """

        email = "test@recepi.com"
        password = "Testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normilized(self):
        """ Test the email for a new user is normilized. """

        email = "test@RECEPI.COM"
        user = get_user_model().objects.create_user(email, "test123")
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """ Test creating an user with invalid email raises error. """

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'Testpass123')

    def test_create_new_superuser(self):
        """ Test creating a new superuser. """

        email = "super@recepi.com"
        password = "test123"
        user = get_user_model().objects.create_superuser(email, password)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_tag(self):
        """ Test a tag string representation. """

        tag = models.Tag.objects.create(user=sample_user(), name="Vegan")
        self.assertEqual(str(tag), tag.name)
