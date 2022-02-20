# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.response import Response  # noqa: E501
from swagger_server.models.role import Role  # noqa: E501
from swagger_server.test import BaseTestCase


class TestCHANGEROLEDETAILSController(BaseTestCase):
    """CHANGEROLEDETAILSController integration test stubs"""

    def test_api_v1_role_role_id_patch(self):
        """Test case for api_v1_role_role_id_patch

        Endpoint to change role
        """
        body = Role()
        response = self.client.open(
            '/api/v1/role/{role_id}'.format(role_id='role_id_example'),
            method='PATCH',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
