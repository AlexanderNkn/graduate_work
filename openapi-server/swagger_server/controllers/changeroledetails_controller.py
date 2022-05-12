import connexion
import six

from swagger_server.models.response import Response  # noqa: E501
from swagger_server.models.role import Role  # noqa: E501
from swagger_server import util


def auth_api_v1_role_role_id_patch(role_id, body=None):  # noqa: E501
    """Endpoint to change role

    change role info # noqa: E501

    :param role_id: Role uuid
    :type role_id: str
    :param body: 
    :type body: dict | bytes

    :rtype: Response
    """
    if connexion.request.is_json:
        body = Role.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
