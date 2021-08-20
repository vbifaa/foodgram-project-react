from django.http import HttpResponseNotFound

from .data.set_data import SetDataClass


class TestWrongUrl(SetDataClass):

    def test_wrong_url(self):
        response = self.guest_client.get('/api/lolkek/')
        
        self.assertIsInstance(response, HttpResponseNotFound)
