from datetime import datetime
from http import HTTPStatus
from operator import itemgetter
from typing import Dict

from flask_restx import marshal
from sqlalchemy import func
from app.database.models.settings import SettingModel
from app import messages
from app.utils.timeUtils import Timeutils
from app.utils.requestID import requestID4response

class SettingDAO:
    """Data Access Object for User functionalities"""
    DEFAULT_PAGE = 1
    DEFAULT_PER_PAGE = 10
    MAX_PER_PAGE = 100

    @staticmethod
    def get_setting(setting_id: int):
        """Retrieves a setting's information using a specified ID.

        Arguments:
            。。。

        Returns:
            。。。

        """
        setting = SettingModel.find_by_id(setting_id)
        setting.creation_date = Timeutils.timeStamp2timeString(setting.creation_date, format="%Y-%m-%d %H:%M:%S")

        return setting

    @staticmethod
    def get_setting_by_key(key: str):
        return SettingModel.find_by_key(key)

    @staticmethod
    def add_setting(data: Dict[str, str]):
        """Add a new setting.

        """

        key = data["key"]
        value = data["value"]

        existing_key = SettingModel.find_by_key(data["key"])
        if existing_key:
            return (
                messages.SETTING_KEY_ALREADY_EXISTS,
                HTTPStatus.CONFLICT,
            )

        setting = SettingModel(key, value)
        setting.save_to_db()

        return messages.SETTING_WAS_ADDED_SUCCESSFULLY, HTTPStatus.CREATED

    @staticmethod
    def delete_setting(setting_id: int):

        setting = SettingModel.find_by_id(setting_id)

        setting.delete_from_db()
        return messages.SETTING_SUCCESSFULLY_DELETED, HTTPStatus.OK


    @staticmethod
    @requestID4response
    def list_settings(
        search_query: str = "",
        page: int = DEFAULT_PAGE,
        per_page: int = DEFAULT_PER_PAGE,
    ):
        """Retrieves a list of setting items with the specified ID.

        """
        setting_list = (
            SettingModel.query.filter(
                func.lower(SettingModel.key).contains(search_query.lower())
                | func.lower(SettingModel.value).contains(search_query.lower()),
            )
            .order_by(SettingModel.id)
            .paginate(
                page=page,
                per_page=per_page,
                error_out=False,
                max_per_page=SettingDAO.MAX_PER_PAGE,
            )
            .items
        )

        setting_list = [setting.json() for setting in setting_list]

        for setting in setting_list:
            # add extra dict into result
            setting['creation_date'] = Timeutils.timeStamp2timeString(setting['creation_date'], format="%Y-%m-%d %H:%M:%S")
            pass

        return setting_list, HTTPStatus.OK

    @staticmethod
    def update_setting(setting_id: int, data: Dict[str, str]):
        """Updates the information of a specified setting ID with new data.

        """
        if "key" in data:
            return {'code': 1011, 'message': 'can not modify key'}, 201

        setting = SettingModel.find_by_id(setting_id)

        setting.value = data["value"]

        setting.save_to_db()

        return messages.SETTING_SUCCESSFULLY_UPDATED, HTTPStatus.OK
    #
    # @staticmethod
    # def get_achievements(user_id: int):
    #     """Shows a subset of the user's achievements
    #
    #     Gets all the completed tasks of the user and
    #     return them in a list. Achievements are completed tasks
    #
    #     Args:
    #         user_id: The ID of the user for whom tasks are
    #             requested.
    #
    #     Returns:
    #         achievements: A list containing the user's achievements
    #     """
    #     user = UserModel.find_by_id(user_id)
    #     all_relations = user.mentor_relations + user.mentee_relations
    #     tasks = []
    #     for relation in all_relations:
    #         tasks += relation.tasks_list.tasks
    #     achievements = [task for task in tasks if task.get("is_done")]
    #     return achievements

    # @staticmethod
    # def get_user_statistics(user_id: int):
    #     """Shows some basic user statistics
    #
    #     Gets the following statistics of the user:
    #     -> Pending Requests
    #     -> Accepted Requests
    #     -> Rejected Requests
    #     -> Completed Relations
    #     -> Cancelled Relations
    #     -> Up to 3 recent achievements
    #
    #     Args:
    #         user_id: The id of the user for whom stats are requested
    #
    #     Returns:
    #         A dict containing the stats (if the user ID is valid)
    #         If user ID is invalid, returns None
    #     """
    #     user = UserModel.find_by_id(user_id)
    #
    #     if not user:
    #         return None
    #
    #     all_relations = user.mentor_relations + user.mentee_relations
    #     (
    #         pending_requests,
    #         accepted_requests,
    #         rejected_requests,
    #         completed_relations,
    #         cancelled_relations,
    #     ) = (0, 0, 0, 0, 0)
    #
    #
    #     achievements = UserDAO.get_achievements(user_id)
    #     if achievements:
    #         # We only need the last three of these achievements
    #         achievements = achievements[-3:]
    #         achievements.sort(key=itemgetter("completed_at"), reverse=True)
    #
    #     response = {
    #         "name": user.name,
    #         "pending_requests": pending_requests,
    #         "accepted_requests": accepted_requests,
    #         "rejected_requests": rejected_requests,
    #         "completed_relations": completed_relations,
    #         "cancelled_relations": cancelled_relations,
    #         "achievements": achievements,
    #     }
    #     return response

