import connexion
import six

from swagger_server.models.response import Response  # noqa: E501
from swagger_server import util


def api_v1_role_role_id_delete(role_id):  # noqa: E501
    """Endpoint to delete role

    delete role # noqa: E501

    :param role_id: Role uuid
    :type role_id: str

    :rtype: Response
    """
    return 'do some magic!'
