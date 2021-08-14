from .data.set_data import SetOneRecipeData


class TestPostRecipe(SetOneRecipeData):

    def test_correct_post_recipe(self):
        response = self.auth_client.post(
            '/api/recipes/', self.recipes[self.recipe_id], format='json'
        )

        self.assert_correct_recipe_response(
            response=response,
            status_code=201,
            correct_data=self.get_recipe_response_data(
                recipe_id=self.recipe_id,
                author_response_data=self.author_data
            )
        )

    def test_not_auth_post_recipe(self):
        response = self.guest_client.post(
            '/api/recipes/', self.recipes[self.recipe_id], format='json'
        )

        self.assert_bad_request(
            response=response,
            status_code=401,
            schema_field='detail' 
        )

    def test_post_recipe_with_not_exist_tag(self):
        recipe = self.recipes[self.recipe_id]
        recipe['tags'].append(len(self.tags) + 1)

        response = self.auth_client.post(
            '/api/recipes/', self.recipes[self.recipe_id], format='json'
        )

        self.assert_bad_request(
            response=response,
            status_code=400,
            schema_field='tags' 
        )
