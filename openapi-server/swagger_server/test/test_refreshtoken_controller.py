# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.response import Response  # noqa: E501
from swagger_server.test import BaseTestCase


class TestREFRESHTOKENController(BaseTestCase):
    """REFRESHTOKENController integration test stubs"""

    def test_api_v1_auth_refresh_token_post(self):
        """Test case for api_v1_auth_refresh_token_post

        Endoint to refresh expired tokens
        """
        response = self.client.open(
            '/api/v1/auth/refresh-token',
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
