from .data.set_data import SetDataClass


class TestTags(SetDataClass):

    def test_get_tags(self):
        self.assert_data_equal_to_api_url_response_data(
            asserter=self.assert_correct_request,
            client=self.guest_client,
            data=self.tags,
            url='tags'
        )

    def test_get_tag(self):
        self.assert_element_from_queryset_equal_url_response(
            asserter=self.assert_correct_request,
            client=self.guest_client,
            queryset=self.tags,
            url='tags'
        )

    def test_not_exist_get_tag(self):
        self.assert_method_get_element_not_exist(
            client=self.guest_client,
            url=f'tags/{len(self.tags) + 1}'
        )
