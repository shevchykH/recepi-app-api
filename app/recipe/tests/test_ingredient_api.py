from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from recipe.serializer import IngredientSerializer
from core.models import Ingredient

INGREDIENT_URL = reverse("recipe:ingredient-list")


class TestIngredientAPI(TestCase):
    """ Test ingredient api. """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test_ingredient@recipe.com",
            password="testpass"
        )
        self.client.force_authenticate(self.user)

    def test_login_required(self):
        client = APIClient()
        res = client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_ingredient_list(self):
        """ Test retrieving ingredients. """

        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.create(user=self.user, name='Sault')

        res = self.client.get(INGREDIENT_URL)

        ingredient = Ingredient.objects.all().order_by("-name")
        serializer = IngredientSerializer(ingredient, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredient_limited_to_user(self):
        """ Test that ingredient is returned for authenticated user. """

        user2 = get_user_model().objects.create_user(
            email="other@recipe.com",
            password="testpass"
        )
        Ingredient.objects.create(
            user=user2,
            name="Sugar"
        )
        ingredient = Ingredient.objects.create(
            user=self.user,
            name="Beet"
        )
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], ingredient.name)
