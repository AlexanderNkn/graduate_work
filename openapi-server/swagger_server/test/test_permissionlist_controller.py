# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.permission import Permission  # noqa: E501
from swagger_server.models.response import Response  # noqa: E501
from swagger_server.test import BaseTestCase


class TestPERMISSIONLISTController(BaseTestCase):
    """PERMISSIONLISTController integration test stubs"""

    def test_api_v1_permission_get(self):
        """Test case for api_v1_permission_get

        Endpoint to get all permissions
        """
        response = self.client.open(
            '/api/v1/permission',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
