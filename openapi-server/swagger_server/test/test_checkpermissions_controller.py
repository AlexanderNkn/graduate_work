# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.response import Response  # noqa: E501
from swagger_server.models.user_role_request import UserRoleRequest  # noqa: E501
from swagger_server.test import BaseTestCase


class TestCHECKPERMISSIONSController(BaseTestCase):
    """CHECKPERMISSIONSController integration test stubs"""

    def test_api_v1_check_permissions_post(self):
        """Test case for api_v1_check_permissions_post

        Endpoint to check user permissions
        """
        body = UserRoleRequest()
        response = self.client.open(
            '/api/v1/check-permissions',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
