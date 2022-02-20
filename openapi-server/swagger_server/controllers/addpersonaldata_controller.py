import connexion
import six

from swagger_server.models.response import Response  # noqa: E501
from swagger_server.models.user_data import UserData  # noqa: E501
from swagger_server import util


def api_v1_auth_personal_data_user_id_post(user_id, body=None):  # noqa: E501
    """Endpoint for user to add personal data

    Additional info about user # noqa: E501

    :param user_id: User id to add/change/delete personal data
    :type user_id: str
    :param body: 
    :type body: dict | bytes

    :rtype: Response
    """
    if connexion.request.is_json:
        body = UserData.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
