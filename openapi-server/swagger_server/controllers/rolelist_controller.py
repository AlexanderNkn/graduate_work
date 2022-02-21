import connexion
import six

from swagger_server.models.response import Response  # noqa: E501
from swagger_server.models.role import Role  # noqa: E501
from swagger_server import util


def auth_api_v1_role_get():  # noqa: E501
    """Endpoint to get all roles

    List of all available roles # noqa: E501


    :rtype: List[Role]
    """
    return 'do some magic!'
