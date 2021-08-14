from .data.set_data import SetOneRecipeData, authentication


class TestPutRecipe(SetOneRecipeData):

    def setUp(self):
        super().setUp()

        self.auth_client.post(
            '/api/recipes/', self.recipes[self.recipe_id], format='json'
        )

    def test_correct_put_recipe(self):
        recipe = self.recipes[self.recipe_id]
        recipe['ingredients'].pop()
        recipe['ingredients'].append({
            'id': 7,
            'amount': 250
        })
        recipe['tags'] = [2, 3]
        recipe['name'] = 'Borsh'
        recipe['cooking_time'] = 25
        recipe['text'] = 'Cook with love'

        response = self.auth_client.put(
            f'/api/recipes/{self.recipe_id + 1}/', recipe, format='json'
        )

        self.assert_correct_recipe_response(
            response=response,
            status_code=200,
            correct_data=self.get_recipe_response_data(
                recipe_id=self.recipe_id,
                author_response_data=self.author_data
            )
        )

    def test_not_auth_put_recipe(self):
        response = self.guest_client.put(
            f'/api/recipes/{self.recipe_id + 1}/',
            self.recipes[self.recipe_id],
            format='json'
        )

        self.assert_bad_request(
            response=response,
            status_code=401,
            schema_field='detail'
        )

    def test_not_author_put_recipe(self):
        self.guest_client.post('/api/users/', self.users[1])
        authentication(self.guest_client, self.get_auth_data(self.users[1]))

        response = self.guest_client.put(
            f'/api/recipes/{self.recipe_id + 1}/',
            self.recipes[self.recipe_id],
            format='json'
        )

        self.assert_bad_request(
            response=response,
            status_code=403,
            schema_field='detail'
        )

    def test_not_exist_put_recipe(self):
        response = self.auth_client.put(
            f'/api/recipes/{self.recipe_id + 2}/',
            self.recipes[self.recipe_id],
            format='json'
        )
        self.assert_bad_request(
            response=response,
            status_code=404,
            schema_field='detail'
        )
