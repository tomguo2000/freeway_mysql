from flask_restx import Model, fields

def add_models_to_namespace(api_namespace):
    api_namespace.models[public_system_setting_model.name] = public_system_setting_model
    api_namespace.models[add_setting_request_body_model.name] = add_setting_request_body_model
    api_namespace.models[update_setting_request_body_model.name] = update_setting_request_body_model


public_system_setting_model = Model(
    "System setting model",
    {
        "id": fields.Integer(
            readOnly=True, description="The unique identifier of a setting item"
        ),
        "key": fields.String(required=True, description="Setting item's name"),
        "value": fields.String(required=True, description="Setting item's value"),
        "creation_date": fields.String(description="Setting item's creation date"),
        "modification_date": fields.String(description="Setting item's last modification date"),
        "last_modification_username": fields.String(description="Setting item's last modification by who?"),
    }
)


add_setting_request_body_model = Model(
    "Add setting request data model",
    {
        "key": fields.String(required=True, description="Setting item's name"),
        "value": fields.String(required=False)
    }

)


update_setting_request_body_model = Model(
    "Update setting request data model",
    {
        "value": fields.String(required=False)
    }

)

