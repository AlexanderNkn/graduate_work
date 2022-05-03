# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.response import Response  # noqa: E501
from swagger_server.test import BaseTestCase


class TestLOGOUTController(BaseTestCase):
    """LOGOUTController integration test stubs"""

    def test_api_v1_auth_logout_post(self):
        """Test case for api_v1_auth_logout_post

        Endpoint to logout user
        """
        response = self.client.open(
            '/auth-api/v1/auth/logout',
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
