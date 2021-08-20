import copy

from recipes.models import Recipe

from .data.set_data import SetAllRecipesData


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

    def test_filter_recipes(self):
        recipes = self.get_recipes_with_tags(Recipe.objects, ['soup'])
        self.assert_filter_recipes('?tags=soup', recipes)

        recipes = self.get_recipes_with_author(Recipe.objects, 1)
        self.assert_filter_recipes('?author=1', recipes)

        recipes = self.get_recipes_with_tags(recipes, ['lunch'])
        self.assert_filter_recipes('?author=1&tags=lunch', recipes)

    def get_recipes_with_tags(self, recipes, tags):
        return recipes.filter(tags__slug__in=tags)

    def get_recipes_with_author(self, recipes, author_id):
        return recipes.filter(author=author_id)

    def assert_filter_recipes(self, url, correct_queryset):
        response_data = self.convert_recipes_queryset_to_dict(correct_queryset)

        response = self.guest_client.get(f'/api/recipes/{url}')

        self.assert_recipes_response(
            response=response,
            status_code=200,
            correct_data=response_data
        )

    def convert_recipes_queryset_to_dict(self, recipes):
        recipes_id = [recipe.id for recipe in recipes]
        recipes_response_data = []
        for recipe in self.recipes:
            if recipe['id'] in recipes_id:
                recipes_response_data.append(copy.deepcopy(recipe))
        return recipes_response_data

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
