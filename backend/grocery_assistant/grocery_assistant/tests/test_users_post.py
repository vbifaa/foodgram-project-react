from .data.set_data import SetAuthUserData, authentication


class TestPostUsers(SetAuthUserData):

    def setUp(self):
        super().setUp()

        self.auth_client_change_password_data = {
            'new_password': 'd3535ac3aAcmfehugnf35efefn',
            'current_password': self.auth_client_data['password']
        }

        self.response = self.guest_client.post('/api/users/', self.auth_client_data)

    def test_post_correct_user(self):
        post_response_data = self.get_user_response_data(self.auth_client_id)
        post_response_data.pop('is_subscribed')

        self.assert_correct_request(
            response=self.response,
            status_code=201,
            correct_data=post_response_data
        )

    def test_post_user_same_email(self):
        another_user_data = self.users[1]
        another_user_data['email'] = self.auth_client_data['email']

        response = self.guest_client.post('/api/users/', another_user_data)

        self.assert_bad_request(response=response, status_code=400, schema_field='email')

    def test_correct_auth(self):
        response = self.guest_client.post(
            '/api/auth/token/login/',
            self.auth_client_auth_data
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('auth_token', response.data)

    def test_wrong_password_auth(self):
        self.auth_client_data['password'] = 'scichpeoa1effa3'

        response = self.guest_client.post(
            '/api/auth/token/login/',
            self.get_auth_data(self.auth_client_data)
        )

        self.assert_bad_request(
            response=response,
            status_code=400,
            schema_field='non_field_errors'
        )

    def test_correct_change_password(self):
        authentication(self.auth_client, self.auth_client_auth_data)

        response = self.auth_client.post(
            '/api/users/set_password/',
            self.auth_client_change_password_data
        )

        self.assert_correct_request(
            response=response,
            status_code=201,
            correct_data=self.auth_client_change_password_data
        )

    def test_wrong_password_change_password(self):
        authentication(self.auth_client, self.auth_client_auth_data)
        self.auth_client_change_password_data['current_password'] = 'llgjbvdc2ss38ascs'

        response = self.auth_client.post(
            '/api/users/set_password/', self.auth_client_change_password_data
        )

        self.assert_bad_request(
            response=response, status_code=400, schema_field='current_password'
        )

    def test_not_auth_change_password(self):
        response = self.guest_client.post(
            '/api/users/set_password/', self.auth_client_change_password_data
        )

        self.assert_bad_request(response=response, status_code=401, schema_field='detail')

    def test_correct_logout(self):
        authentication(self.auth_client, self.auth_client_auth_data)

        response_logout = self.auth_client.post('/api/auth/token/logout/')
        response_use_bad_token = self.auth_client.post(
            '/api/users/set_password/', self.auth_client_change_password_data
        )

        self.assertEqual(response_logout.status_code, 204)
        self.assert_bad_request(
            response=response_use_bad_token, status_code=401, schema_field='detail'
        )

    def test_not_auth_logout(self):
        response = self.guest_client.post('/api/auth/token/logout/')

        self.assert_bad_request(response=response, status_code=401, schema_field='detail')
