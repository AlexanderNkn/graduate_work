# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.response import Response  # noqa: E501
from swagger_server.test import BaseTestCase


class TestLOGINHISTORYController(BaseTestCase):
    """LOGINHISTORYController integration test stubs"""

    def test_api_v1_auth_login_history_user_id_get(self):
        """Test case for api_v1_auth_login_history_user_id_get

        Endoint to get history of user logouts
        """
        response = self.client.open(
            '/api/v1/auth/login-history/{user_id}'.format(user_id='user_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
