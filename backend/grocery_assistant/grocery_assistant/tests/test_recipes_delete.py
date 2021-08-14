from .data.set_data import SetOneRecipeData, authentication


class TestDeleteRecipe(SetOneRecipeData):
    
    def setUp(self):
        super().setUp()

        self.recipe_id = 0
        self.auth_client.post(
            '/api/recipes/', self.recipes[self.recipe_id], format='json'
        )

    def test_correct_delete_recipe(self):
        response = self.auth_client.delete(f'/api/recipes/{self.recipe_id + 1}/')
        
        self.assert_correct_request(
            response=response,
            status_code=204,
            correct_data=None
        )

    def test_not_auth_delete_recipe(self):
        response = self.guest_client.delete(f'/api/recipes/{self.recipe_id + 1}/')

        self.assert_bad_request(
            response=response,
            status_code=401,
            schema_field='detail'
        )

    def test_not_author_delete_recipe(self):
        self.guest_client.post('/api/users/', self.users[1])
        authentication(self.guest_client, self.get_auth_data(self.users[1]))

        response = self.guest_client.delete(f'/api/recipes/{self.recipe_id + 1}/')

        self.assert_bad_request(
            response=response,
            status_code=403,
            schema_field='detail'
        )

    def test_not_exist_delete_recipe(self):
        response = self.auth_client.delete(f'/api/recipes/{self.recipe_id + 2}/')

        self.assert_bad_request(
            response=response,
            status_code=404,
            schema_field='detail'
        )
