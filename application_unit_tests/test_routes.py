from flask_testing import TestCase
from app import app


# subclass this instead of TestCase
class CreateAppHelperClass(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

class NotFoundRoute(CreateAppHelperClass):
    def test_route_response(self):
        resp = self.client.get('/some_not_existing_endpoint/')
        self.assert404(resp)
        self.assertEqual(resp.json, dict(error='Not found'))

