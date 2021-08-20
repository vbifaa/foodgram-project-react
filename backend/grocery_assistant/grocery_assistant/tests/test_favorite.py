#simple tests

from .data.set_data import SetAllRecipesData


class TestFavorite(SetAllRecipesData):

    def test_create_favorite(self):
        response = self.auth_client.get('/api/recipes/1/favorite/')

        self.assertEqual(response.status_code, 201)

    def test_delete_favorite(self):
        self.auth_client.get('/api/recipes/1/favorite/')
        response = self.auth_client.delete('/api/recipes/1/favorite/')

        self.assertEqual(response.status_code, 204)
