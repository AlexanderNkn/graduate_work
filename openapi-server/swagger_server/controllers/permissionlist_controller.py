import connexion
import six

from swagger_server.models.permission import Permission  # noqa: E501
from swagger_server.models.response import Response  # noqa: E501
from swagger_server import util


def api_v1_permission_get():  # noqa: E501
    """Endpoint to get all permissions

    List of all available permissions # noqa: E501


    :rtype: List[Permission]
    """
    return 'do some magic!'
