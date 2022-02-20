import connexion
import six

from swagger_server.models.response import Response  # noqa: E501
from swagger_server import util


def api_v1_auth_delete_personal_data_user_id_delete(user_id):  # noqa: E501
    """Endpoint to delete user personal data

    Additional info about user # noqa: E501

    :param user_id: User id to add/change/delete personal data
    :type user_id: str

    :rtype: Response
    """
    return 'do some magic!'
