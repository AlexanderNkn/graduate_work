# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.response import Response  # noqa: E501
from swagger_server.models.role import Role  # noqa: E501
from swagger_server.test import BaseTestCase


class TestCREATEROLEController(BaseTestCase):
    """CREATEROLEController integration test stubs"""

    def test_api_v1_role_post(self):
        """Test case for api_v1_role_post

        Endpoint to create new role
        """
        body = Role()
        response = self.client.open(
            '/auth-api/v1/role',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
