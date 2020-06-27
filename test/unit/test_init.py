from test.unit.fixtures import TestRoute


class TestIndex(TestRoute):
    def test_should_return_not_found_on_index_route(self):
        response = self.client.get("/")
        self.assertEqual({"detail": "Not Found"}, response.json())
        self.assertEqual(404, response.status_code)
