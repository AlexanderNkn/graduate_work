# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class UserRoleRequest(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, role_ids: List[str]=None, user_id: str=None):  # noqa: E501
        """UserRoleRequest - a model defined in Swagger

        :param role_ids: The role_ids of this UserRoleRequest.  # noqa: E501
        :type role_ids: List[str]
        :param user_id: The user_id of this UserRoleRequest.  # noqa: E501
        :type user_id: str
        """
        self.swagger_types = {
            'role_ids': List[str],
            'user_id': str
        }

        self.attribute_map = {
            'role_ids': 'role_ids',
            'user_id': 'user_id'
        }
        self._role_ids = role_ids
        self._user_id = user_id

    @classmethod
    def from_dict(cls, dikt) -> 'UserRoleRequest':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The UserRoleRequest of this UserRoleRequest.  # noqa: E501
        :rtype: UserRoleRequest
        """
        return util.deserialize_model(dikt, cls)

    @property
    def role_ids(self) -> List[str]:
        """Gets the role_ids of this UserRoleRequest.


        :return: The role_ids of this UserRoleRequest.
        :rtype: List[str]
        """
        return self._role_ids

    @role_ids.setter
    def role_ids(self, role_ids: List[str]):
        """Sets the role_ids of this UserRoleRequest.


        :param role_ids: The role_ids of this UserRoleRequest.
        :type role_ids: List[str]
        """

        self._role_ids = role_ids

    @property
    def user_id(self) -> str:
        """Gets the user_id of this UserRoleRequest.


        :return: The user_id of this UserRoleRequest.
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id: str):
        """Sets the user_id of this UserRoleRequest.


        :param user_id: The user_id of this UserRoleRequest.
        :type user_id: str
        """

        self._user_id = user_id
