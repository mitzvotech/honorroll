from unittest import TestCase
import pytest
from flask.ext.webtest import TestApp
from honorroll.app.app import create_app

from flask import url_for


class TestFrontend:

    def test_frontend_access(self, client):
        res = client.get(url_for('frontend.index'))
        assert res.status_code == 200

#
# class ExampleTest(TestCase):
#     def setUp(self):
#         self.app = app
#         self.app.config["TEST"] = True
#         self.w = TestApp(self.app)
#
#     def test(self):
#         r = self.w.get('/')
#         # Assert there was no messages flushed:
#         self.assertFalse(r.flashes)
#         # Access and check any variable from template context...
#         self.assertEqual(r.context['text'], 'Hello!')
#         self.assertEqual(r.template, 'template.html')
#         # ...and from session
