# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server.models.response import Response  # noqa: E501
from swagger_server.models.user_role_request import UserRoleRequest  # noqa: E501
from swagger_server.test import BaseTestCase


class TestCHECKROLESController(BaseTestCase):
    """CHECKROLESController integration test stubs"""

    def test_api_v1_check_roles_post(self):
        """Test case for api_v1_check_roles_post

        Endpoint to check user roles
        """
        body = UserRoleRequest()
        response = self.client.open(
            '/auth-api/v1/check-roles',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
