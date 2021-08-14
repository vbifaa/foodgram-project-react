from .data.set_data import SetAllRecipesData

#  Надо рефакторить и добавить тесты на фильтры

class TestGetRecipe(SetAllRecipesData):

    def test_get_without_params_recipes(self):
        self.assert_data_equal_to_api_url_response_data(
            asserter=self.assert_recipes_response,
            client=self.auth_client,
            data=self.recipes,
            url='recipes'
        )

    def test_get_with_params_limit_2_recipes(self):
        response = self.guest_client.get('/api/recipes/?page=1&limit=2')

        self.assertIn('results', response.data)
        results = response.data.pop('results')

        self.assert_correct_request(
            response=response,
            status_code=200,
            correct_data={
                'count': 2,
                'next': None,
                'previous': None
            }
        )
        response.data = results
        self.assert_recipes_response(
            response=response,
            status_code=200,
            correct_data=self.recipes
        )

    def test_get_with_params_limit_1_recipes(self):
        response_first_page = self.guest_client.get('/api/recipes/?page=1&limit=1')
        response_second_page = self.guest_client.get('/api/recipes/?page=2&limit=1')

        for response in [response_first_page, response_second_page]:
            self.assertIn('results', response.data)
            
        results = response_first_page.data.pop('results')
        self.assert_correct_request(
            response=response_first_page,
            status_code=200,
            correct_data={
                'count': 2,
                'next': 'http://testserver/api/recipes/?limit=1&page=2',
                'previous': None
            }
        )
        response_first_page.data = results
        self.assert_recipes_response(
            response=response_first_page,
            status_code=200,
            correct_data=[self.recipes[0]]
        )

        results = response_second_page.data.pop('results')
        self.assert_correct_request(
            response=response_second_page,
            status_code=200,
            correct_data={
                'count': 2,
                'next': None,
                'previous': 'http://testserver/api/recipes/?limit=1'
            }
        )
        response_second_page.data = results
        self.assert_recipes_response(
            response=response_second_page,
            status_code=200,
            correct_data=[self.recipes[1]]
        )

    def test_get_recipe(self):
        self.assert_element_from_queryset_equal_url_response(
            asserter=self.assert_correct_recipe_response,
            client=self.guest_client,
            queryset=self.recipes,
            url='recipes'
        )

    def test_not_exist_get_recipe(self):
        self.assert_method_get_element_not_exist(
            client=self.guest_client,
            url=f'recipes/{len(self.recipes) + 1}'
        )
