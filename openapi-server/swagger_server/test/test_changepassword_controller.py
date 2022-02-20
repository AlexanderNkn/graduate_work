# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.passwords import Passwords  # noqa: E501
from swagger_server.models.response import Response  # noqa: E501
from swagger_server.test import BaseTestCase


class TestCHANGEPASSWORDController(BaseTestCase):
    """CHANGEPASSWORDController integration test stubs"""

    def test_api_v1_auth_change_password_user_id_patch(self):
        """Test case for api_v1_auth_change_password_user_id_patch

        Endpoint to change forgotten password
        """
        body = Passwords()
        response = self.client.open(
            '/api/v1/auth/change-password/{user_id}'.format(user_id='user_id_example'),
            method='PATCH',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
