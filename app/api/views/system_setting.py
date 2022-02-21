from http import HTTPStatus
from flask import request
from flask_restx import Namespace, Resource, marshal, Model, fields
from app import messages

from app.api.models.system_setting import (
    add_models_to_namespace,
    public_system_setting_model,
    add_setting_request_body_model,
    update_setting_request_body_model
)
from app.api.validations.setting import (
    validate_setting_add_request_data,
    validate_setting_update_request_data
)


from app.api.dao.system_setting import SettingDAO


setting_ns = Namespace("Settings", description="Operations related to users")
add_models_to_namespace(setting_ns)


DAO = SettingDAO()


@setting_ns.route("settings")
class SettingList(Resource):
    @classmethod
    @setting_ns.doc(
        "list_settings",
        params={
            "search": "Search query",
            "page": "specify page of users (default: 1)",
            "per_page": "specify number of setting per page (default: 10)",
        },
    )
    @setting_ns.response(
        HTTPStatus.OK.value,
        f"{messages.GENERAL_SUCCESS_MESSAGE}",
        public_system_setting_model,
    )
    @setting_ns.marshal_list_with(
        public_system_setting_model, code=HTTPStatus.OK.value, description="Success"
    )
    def get(self):

        page = request.args.get("page", default=SettingDAO.DEFAULT_PAGE, type=int)
        per_page = request.args.get(
            "per_page", default=SettingDAO.DEFAULT_PER_PAGE, type=int
        )

        return DAO.list_settings(request.args.get("search", ""), page, per_page)


@setting_ns.route("add")
class SettingAdd(Resource):
    @classmethod
    @setting_ns.expect(add_setting_request_body_model, validate=True)
    def post(cls):

        data = request.json

        is_valid = validate_setting_add_request_data(data)

        if is_valid != {}:
            return is_valid, HTTPStatus.BAD_REQUEST

        result = DAO.add_setting(data)

        return result


@setting_ns.route("settings/<int:setting_id>")
@setting_ns.param("setting_id", "The setting identifier")
class SettingsB(Resource):
    @classmethod
    @setting_ns.doc("get_setting")
    @setting_ns.response(
        HTTPStatus.OK.value,
        f"{messages.GENERAL_SUCCESS_MESSAGE}",
        public_system_setting_model,
    )
    @setting_ns.response(
        HTTPStatus.UNAUTHORIZED.value,
        f"{messages.TOKEN_HAS_EXPIRED}\n"
        f"{messages.TOKEN_IS_INVALID}\n"
        f"{messages.AUTHORISATION_TOKEN_IS_MISSING}",
    )
    @setting_ns.response(HTTPStatus.NOT_FOUND.value, f"{messages.USER_DOES_NOT_EXIST}")
    def get(cls, setting_id):
        """
        Returns a setting.
        """
        requested_setting = DAO.get_setting(setting_id)
        if isinstance(requested_setting, tuple):
            return requested_setting
        else:
            return marshal(requested_setting, public_system_setting_model), HTTPStatus.OK


    @classmethod
    @setting_ns.doc("update_user_profile")
    @setting_ns.expect(update_setting_request_body_model)
    def put(cls, setting_id):
        """
        """
        data = request.json
        is_valid = validate_setting_update_request_data(data)

        if is_valid != {}:
            return is_valid, 400

        return DAO.update_setting(setting_id, data)

    @classmethod
    @setting_ns.doc("delete_user")
    def delete(cls, setting_id):
        """
        """
        return DAO.delete_setting(setting_id)
