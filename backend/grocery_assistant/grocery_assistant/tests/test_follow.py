#simple tests

from users.models import Follow

from .data.set_data import SetAllRecipesData


class TestFollow(SetAllRecipesData):

    def test_create_follow(self):
        response = self.auth_client.get('/api/users/2/subscribe/')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(Follow.objects.all()), 1)
        self.assertIsNotNone(Follow.objects.get(id=1))

    def test_delete_follow(self):
        self.auth_client.get('/api/users/2/subscribe/')
        response = self.auth_client.delete('/api/users/2/subscribe/')

        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(Follow.objects.all()), 0)
