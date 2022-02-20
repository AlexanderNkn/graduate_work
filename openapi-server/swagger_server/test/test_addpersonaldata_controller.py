# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.response import Response  # noqa: E501
from swagger_server.models.user_data import UserData  # noqa: E501
from swagger_server.test import BaseTestCase


class TestADDPERSONALDATAController(BaseTestCase):
    """ADDPERSONALDATAController integration test stubs"""

    def test_api_v1_auth_add_personal_data_user_id_post(self):
        """Test case for api_v1_auth_add_personal_data_user_id_post

        Endpoint for user to add personal data
        """
        body = UserData()
        response = self.client.open(
            '/api/v1/auth/add-personal-data/{user_id}'.format(user_id='user_id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
