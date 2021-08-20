import copy

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from . import objects_creator
from .assertions import Assertions
from .data import Data


def authentication(client, client_auth_data):
    token = client.post('/api/auth/token/login/', client_auth_data).data['auth_token']
    client.credentials(HTTP_AUTHORIZATION='Token ' + token)


class SetDataClass(Assertions):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.tags = objects_creator.create_objects(
            creator=objects_creator.tag_creator,
            objects=Data.tags
        )
        cls.ingredients = objects_creator.create_objects(
            creator=objects_creator.ingredient_creator,
            objects=Data.ingredients
        )
        cls.users = copy.deepcopy(Data.users)

    def setUp(self):
        super().setUp()

        self.guest_client = APIClient()


class SetAuthUserData(SetDataClass):

    def setUp(self):
        super().setUp()

        self.auth_client = APIClient()
        self.auth_client_id = 0
        self.auth_client_data = self.users[self.auth_client_id]
        self.auth_client_auth_data = self.get_auth_data(self.auth_client_data)

    def get_user_response_data(self, user_id):
        response_data = self.users[user_id].copy()

        response_data.pop('password')
        response_data['id'] = user_id + 1
        response_data['is_subscribed'] = False

        return response_data

    def get_auth_data(self, user_data):
        auth_data = {
            'email': user_data['email'],
            'password': user_data['password']
        }
        return auth_data


class SetOneRecipeData(SetAuthUserData):

    def setUp(self):
        super().setUp()
        
        self.recipes = copy.deepcopy(Data.recipes)
        
        self.recipe_id = 0

        self.guest_client.post('/api/users/', self.auth_client_data)
        authentication(self.auth_client, self.auth_client_auth_data)
        self.author_data = self.get_user_response_data(self.auth_client_id)

    def get_recipe_response_data(self, recipe_id, author_response_data):
        response_data = self.recipes[recipe_id].copy()

        for ingredient in response_data['ingredients']:
            id = ingredient['id']
            ingredient.update(self.ingredients[id - 1])

        response_tags = []
        for tag_id in response_data['tags']:
            response_tags.append(self.tags[tag_id - 1])
        response_data['tags'] = response_tags

        response_data['id'] = recipe_id + 1
        response_data['is_favorited'] = False
        response_data['is_in_shopping_cart'] = False
        response_data['author'] = author_response_data
        response_data.pop('image')

        return response_data


class SetAllRecipesData(SetOneRecipeData):

    def setUp(self):
        super().setUp()

        self.second_auth_client = APIClient()
        self.second_auth_client_id = 1
        self.second_auth_client_data = self.users[
            self.second_auth_client_id
        ]

        self.second_auth_client_auth_data = (
            self.get_auth_data(self.second_auth_client_data)
        )
        self.guest_client.post('/api/users/', self.second_auth_client_data)
        authentication(
            self.second_auth_client, self.second_auth_client_auth_data
        )
 
        mid = len(self.recipes) // 2
        self.client_post_recipes(
            client=self.auth_client,
            range=range(0, mid),
            author_id=self.auth_client_id
        )
        self.client_post_recipes(
            client=self.second_auth_client,
            range=range(mid, len(self.recipes)),
            author_id=self.second_auth_client_id
        )

    def client_post_recipes(self, client, range, author_id):
        for recipe_id in range:
            self.recipes[recipe_id] = self.post_recipe(
                client, self.recipes[recipe_id], recipe_id, author_id
            )

    def post_recipe(self, client, recipe, recipe_id, author_id):
        client.post('/api/recipes/', recipe, format='json')
        author_response_data = self.get_user_response_data(author_id)
        recipe = self.get_recipe_response_data(recipe_id, author_response_data)
        return recipe
