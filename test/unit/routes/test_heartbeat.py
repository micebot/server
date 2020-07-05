from test.unit.fixtures import TestRoute


class TestHeartbeat(TestRoute):
    def test_should_return_valid_when_authenticated(self):
        response = self.client.get("/hb")
        self.assertEqual(200, response.status_code)
        self.assertEqual({"valid": True}, response.json())
