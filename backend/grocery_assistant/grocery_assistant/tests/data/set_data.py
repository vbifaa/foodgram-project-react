from rest_framework.test import APIClient
from .data import Data
from .assertions import Assertions
from .objects_creator import create_objects, tag_creator, ingredient_creator


def authentication(client, client_auth_data):
    token = client.post('/api/auth/token/login/', client_auth_data).data['auth_token']
    client.credentials(HTTP_AUTHORIZATION='Token ' + token)


class SetDataClass(Assertions):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.tags = create_objects(
            creator=tag_creator,
            objects=Data.tags
        )

        cls.ingredients = create_objects(
            creator=ingredient_creator,
            objects=Data.ingredients
        )

    def setUp(self):
        super().setUp()

        self.guest_client = APIClient()
        self.auth_client = APIClient()
        self.users = Data.users
        self.auth_client_id = 0
        self.auth_client_data = self.users[self.auth_client_id]
        
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
