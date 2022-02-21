from flask import Flask
from flask_migrate import Migrate
from config import get_env_config
from app.utils.requestID import requestID4response


def create_app(config_filename: str) -> Flask:

    from app.utils.setLogger import init_logger
    init_logger()

    app = Flask(__name__)

    # setup application environment
    app.config.from_object(config_filename)
    app.url_map.strict_slashes = False

    from app.schedulers.background_scheduler import init_schedulers
    init_schedulers()

    from app.database.sqlalchemy_extension import db
    db.init_app(app)
    migrate = Migrate(app, db)  # noqa: F841

    # from app.api.jwt_extension import jwt
    #
    # jwt.init_app(app)

    from app.api.api_all import api
    api.init_app(app)

    from app.api.mail_extension import mail
    mail.init_app(app)

    from app.schedulers.background_scheduler import init_schedulers
    init_schedulers()

    return app


application = create_app(get_env_config())


@application.before_first_request
def create_tables():
    from app.database.sqlalchemy_extension import db

    db.create_all()


@application.route("/a", methods=['GET'])
@requestID4response
def aaa():
    from app.utils.setLogger import logger
    logger.info("/a happen******************************************************************************")
    return {'code': 200, 'message': 'good'}, 200


if __name__ == "__main__":
    application.run(port=5005, use_reloader=False)
