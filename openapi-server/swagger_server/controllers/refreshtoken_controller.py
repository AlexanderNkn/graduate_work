import connexion
import six

from swagger_server.models.response import Response  # noqa: E501
from swagger_server import util


def api_v1_auth_refresh_token_post():  # noqa: E501
    """Endoint to refresh expired tokens

    Refresh expired tokens # noqa: E501


    :rtype: Response
    """
    return 'do some magic!'
