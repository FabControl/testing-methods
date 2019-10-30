from flask_testing import TestCase
from app import app

class NotFoundRoute(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_route_response(self):
        resp = self.client.get('/some_not_existing_endpoint/')
        self.assert404(resp)
        self.assertEqual(resp.json, dict(error='Not found'))

