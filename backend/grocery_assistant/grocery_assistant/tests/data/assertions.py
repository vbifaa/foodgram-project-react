from django.test import TestCase
from typing import List
import copy

class Assertions(TestCase):
    
    def setUp(self):
        super().setUp()
        self.maxDiff = None

    def assert_bad_request(self, response, status_code, schema_field):
        self.assertEqual(response.status_code, status_code)
        self.assertIn(schema_field, response.data)

    def assert_correct_request(self, response, status_code, correct_data):
        self.assertEqual(response.status_code, status_code)
        if isinstance(correct_data, List):
            self.assertCountEqual(response.data, correct_data)
        else:
            self.assertEqual(response.data, correct_data)

    def assert_correct_recipe_response(self, response, status_code, correct_data):
        self.assertIn('image', response.data)
        response.data.pop('image')

        for field_name in ['ingredients', 'tags']:
            self.assertCountEqual(response.data[field_name], correct_data[field_name])
            correct_data.pop(field_name)
            response.data.pop(field_name)

        self.assert_correct_request(response, status_code, correct_data)

    def assert_recipes_response(self, response, status_code, correct_data):
        self.assertEqual(len(response.data), len(correct_data))
        
        key = lambda x: x['id']
        response.data.sort(key=key, reverse=True)
        correct_data.sort(key=key, reverse=True)

        for id in range(len(correct_data)):
            recipe_response = copy.deepcopy(response)
            recipe_response.data = response.data[id]
            self.assert_correct_recipe_response(recipe_response, status_code, correct_data[id])

    def assert_data_equal_to_api_url_response_data(self, asserter, client, data, url):
        response = client.get(f'/api/{url}/')

        asserter(response=response, status_code=200, correct_data=data)

    def assert_element_from_queryset_equal_url_response(self, asserter, client, queryset, url):
        for id in range(len(queryset)):
            response = client.get(f'/api/{url}/{id + 1}/')

            asserter(
                response=response,
                status_code=200,
                correct_data=queryset[id]
            )

    def assert_method_get_element_not_exist(self, client, url):
        response = client.get(f'/api/{url}/')

        self.assert_bad_request(
            response=response,
            status_code=404,
            schema_field='detail'
        )
