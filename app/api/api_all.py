from flask_restx import Api
from app.api.views.system_setting import setting_ns as setting_namespace

api = Api(
    title="Freeway Demo API",
    version="1.0",
    description="API documentation for the backend of freeway System. \n \n"
    + "Freeway System is an application that demo all basic featchers are needed,"
    " through 1:1 relations during a certain period of time. \n \n",
)

api.namespaces.clear()

api.add_namespace(setting_namespace, path="/")
