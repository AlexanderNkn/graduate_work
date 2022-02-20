# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.credentials import Credentials  # noqa: E501
from swagger_server.models.response import Response  # noqa: E501
from swagger_server.test import BaseTestCase


class TestREGISTRATIONController(BaseTestCase):
    """REGISTRATIONController integration test stubs"""

    def test_api_v1_auth_register_post(self):
        """Test case for api_v1_auth_register_post

        Endpoint to register new account
        """
        body = Credentials()
        response = self.client.open(
            '/api/v1/auth/register',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
