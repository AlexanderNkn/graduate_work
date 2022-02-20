import connexion
import six

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.response import Response  # noqa: E501
from swagger_server.models.user_role_request import UserRoleRequest  # noqa: E501
from swagger_server import util


def api_v1_check_permission_post(body=None):  # noqa: E501
    """Endpoint to check user permissions

    check if user belongs to specified permission # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: InlineResponse200
    """
    if connexion.request.is_json:
        body = UserRoleRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
