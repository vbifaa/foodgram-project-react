from .data.set_data import SetAuthUserData, authentication


class TestGetUsers(SetAuthUserData):

    def setUp(self):
        super().setUp()

        for user in self.users:
            self.guest_client.post('/api/users/', user)

        authentication(self.auth_client, self.get_auth_data(self.auth_client_data))

        self.users_response_data = [
            self.get_user_response_data(user_id) for user_id in range(len(self.users))
        ]

    def test_get_without_params_users(self):
        self.assert_data_equal_to_api_url_response_data(
            asserter=self.assert_correct_request,
            client=self.guest_client,
            data=self.users_response_data,
            url='users'
        )

    def test_get_with_params_limit_2_users(self):
        response = self.guest_client.get('/api/users/?page=1&limit=2')

        self.assert_correct_request(
            response=response,
            status_code=200,
            correct_data={
                'count': 2,
                'next': None,
                'previous': None,
                'results': self.users_response_data
            }
        )

    def test_get_with_params_limit_1_users(self):
        response_first_page = self.guest_client.get('/api/users/?page=1&limit=1')
        response_second_page = self.guest_client.get('/api/users/?page=2&limit=1')

        self.assert_correct_request(
            response=response_first_page,
            status_code=200,
            correct_data={
                'count': 2,
                'next': 'http://testserver/api/users/?limit=1&page=2',
                'previous': None,
                'results': [self.users_response_data[0]]
            }
        )
        self.assert_correct_request(
            response=response_second_page,
            status_code=200,
            correct_data={
                'count': 2,
                'next': None,
                'previous': 'http://testserver/api/users/?limit=1',
                'results': [self.users_response_data[1]]
            }
        )

    def test_correct_get_user(self):
        self.assert_element_from_queryset_equal_url_response(
            asserter=self.assert_correct_request,
            client=self.auth_client,
            queryset=self.users_response_data,
            url='users'
        )

    def test_correct_get_current_user(self):
        response = self.auth_client.get('/api/users/me/')

        self.assert_correct_request(
            response=response, 
            status_code=200, 
            correct_data=self.get_user_response_data(self.auth_client_id)
        )

    def test_not_exist_get_user(self):
        self.assert_method_get_element_not_exist(
            client=self.auth_client,
            url='users/3'
        )

    def test_not_auth_get_user(self):
        response = self.guest_client.get('/api/users/1/')

        self.assert_bad_request(response=response, status_code=401, schema_field='detail')

    def test_not_auth_get_current_user(self):
        response = self.guest_client.get('/api/users/me/')

        self.assert_bad_request(response=response, status_code=401, schema_field='detail')
