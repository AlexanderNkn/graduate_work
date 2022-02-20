import connexion
import six

from swagger_server.models.response import Response  # noqa: E501
from swagger_server import util


def api_v1_auth_login_history_user_id_get(user_id):  # noqa: E501
    """Endpoint to get history of user logouts

    info about user login # noqa: E501

    :param user_id: User id to view login history
    :type user_id: str

    :rtype: Response
    """
    return 'do some magic!'
