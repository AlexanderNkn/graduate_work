# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.response import Response  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDELETEROLEController(BaseTestCase):
    """DELETEROLEController integration test stubs"""

    def test_api_v1_role_role_id_delete(self):
        """Test case for api_v1_role_role_id_delete

        Endpoint to delete role
        """
        response = self.client.open(
            '/api/v1/role/{role_id}'.format(role_id='role_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
