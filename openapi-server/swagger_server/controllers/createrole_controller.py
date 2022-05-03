import connexion
import six

from swagger_server.models.response import Response  # noqa: E501
from swagger_server.models.role import Role  # noqa: E501
from swagger_server import util


def auth_api_v1_role_post(body=None):  # noqa: E501
    """Endpoint to create new role

    Create new role # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: Response
    """
    if connexion.request.is_json:
        body = Role.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
