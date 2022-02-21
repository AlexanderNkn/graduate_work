import connexion
import six

from swagger_server.models.response import Response  # noqa: E501
from swagger_server.models.user_role_request import UserRoleRequest  # noqa: E501
from swagger_server import util


def auth_api_v1_assign_roles_post(body=None):  # noqa: E501
    """Endpoint to assign roles to user

    Assign roles to user # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: Response
    """
    if connexion.request.is_json:
        body = UserRoleRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
