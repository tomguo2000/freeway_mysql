from app import messages
from app.api.validations.common import *

def validate_setting_add_request_data(data):
    # Verify if request body has required fields
    if "key" not in data:
        return {"message": "key is missing"}
    if "value" not in data:
        return {"message": "value is missing"}

    key = data["key"]
    value = data["value"]

    if not (
        isinstance(key, str)
        and isinstance(value, str)
    ):
        return {"message": "key and value must be string"}

    return {}


def validate_setting_update_request_data(data):
    print(data)

    if not data:
        return messages.NO_DATA_FOR_UPDATING_PROFILE_WAS_SENT

    if "key" in data:
        return {"message": "key can not be modify"}
    if "value" not in data:
        return {"code": 12000, "message": "value is missing"}

    if include_dangerous_chars(data['value']):
        return messages.INVALID_INPUT

    return {}
