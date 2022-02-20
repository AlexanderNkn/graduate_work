import connexion
import six

from swagger_server.models.passwords import Passwords  # noqa: E501
from swagger_server.models.response import Response  # noqa: E501
from swagger_server import util


def api_v1_auth_change_password_user_id_patch(user_id, body=None):  # noqa: E501
    """Endpoint to change forgotten password

    Change user password # noqa: E501

    :param user_id: User id to change history
    :type user_id: str
    :param body: 
    :type body: dict | bytes

    :rtype: Response
    """
    if connexion.request.is_json:
        body = Passwords.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
