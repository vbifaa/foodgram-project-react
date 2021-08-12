from .data.set_data import SetDataClass


class TestIngredients(SetDataClass):

    def test_get_without_params_ingredients(self):
        self.assert_data_equal_to_api_url_response_data(
            client=self.guest_client,
            data=self.ingredients,
            url='ingredients'
        )

    def test_get_ingredients_start_with(self):
        self.assert_get_ingredients_start_with('М')
        self.assert_get_ingredients_start_with('Пом')
        self.assert_get_ingredients_start_with('Соль')

    def assert_get_ingredients_start_with(self, word):
        ingredients_response_data = self.get_ingredients_start_with(word)

        response = self.guest_client.get(f'/api/ingredients/?name={word}')

        self.assert_correct_request(
            response=response,
            status_code=200,
            correct_data=ingredients_response_data
        )

    def get_ingredients_start_with(self, word):
        ingredients_response_data = []
        for ingredient in self.ingredients:
            if ingredient['name'][:len(word)] == word:
                ingredients_response_data.append(ingredient)

        return ingredients_response_data

    def test_get_ingredient(self):
        self.assert_element_from_queryset_equal_url_response(
            client=self.guest_client,
            queryset=self.ingredients,
            url='ingredients'
        )

    def test_not_exist_get_ingredient(self):
        self.assert_element_not_exist(
            client=self.guest_client,
            url=f'ingredients/{len(self.ingredients) + 1}'
        )
