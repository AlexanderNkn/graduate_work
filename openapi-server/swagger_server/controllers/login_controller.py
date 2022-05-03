import connexion
import six

from swagger_server.models.credentials import Credentials  # noqa: E501
from swagger_server.models.response import Response  # noqa: E501
from swagger_server import util


def auth_api_v1_auth_login_post(body=None):  # noqa: E501
    """Endpoint for user login

    Get JWT tokens after login # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: Response
    """
    if connexion.request.is_json:
        body = Credentials.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
