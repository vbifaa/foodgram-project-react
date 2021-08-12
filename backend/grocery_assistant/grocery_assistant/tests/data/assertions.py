from django.test import TestCase
from typing import List

class Assertions(TestCase):

    def assert_bad_request(self, response, status_code, schema_field):
        self.assertEqual(response.status_code, status_code)
        self.assertIn(schema_field, response.data)

    def assert_correct_request(self, response, status_code, correct_data):
        self.assertEqual(response.status_code, status_code)
        if isinstance(correct_data, List):
            self.assertCountEqual(response.data, correct_data)
        else:
            self.assertEqual(response.data, correct_data)

    def assert_data_equal_to_api_url_response_data(self, client, data, url):
        response = client.get(f'/api/{url}/')

        self.assert_correct_request(
            response=response,
            status_code=200,
            correct_data=data
        )

    def assert_element_from_queryset_equal_url_response(self, client, queryset, url):
        for id in range(len(queryset)):
            response = client.get(f'/api/{url}/{id + 1}/')

            self.assert_correct_request(
                response=response,
                status_code=200,
                correct_data=queryset[id]
            )

    def assert_element_not_exist(self, client, url):
        response = client.get(f'/api/{url}/')

        self.assert_bad_request(
            response=response,
            status_code=404,
            schema_field='detail'
        )
