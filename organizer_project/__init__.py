import warnings
from typing import TYPE_CHECKING

from flask import Flask, Response, redirect, request
# from flask_caching import Cache
from flask_marshmallow import Marshmallow
from flask_smorest import Api
# from flask_sqlalchemy import SQLAlchemy

from organizer_project.config import (
    CACHING_OPTIONS,
    DB_URL,
    DEBUG,
    DEV,
    FLASK_DEV_CONFIG,
    FLASK_PROD_CONFIG,
    FLASK_TEST_CONFIG,
    JWT_SECRET_KEY,
    OLD_API_SERVER,
    POSTGRES_DB,
    POSTGRES_PW,
    POSTGRES_URL,
    POSTGRES_USER,
    SENTRY_DSN,
    STATIC_FOLDER,
    SQLALCHEMY_ENGINE_OPTIONS,
)
# from som.types.db import MarketModel, MarketQuery

# if TYPE_CHECKING:
    # from som.models import User

# if SENTRY_DSN:
#     sentry_sdk.init(
#         dsn=SENTRY_DSN,
#         integrations=[FlaskIntegration()],
#         traces_sample_rate=1.0,
#     )

app = Flask(__name__, static_folder=STATIC_FOLDER)
app.config.update(**FLASK_DEV_CONFIG)
# db = SQLAlchemy(
#     app,
#     model_class=MarketModel,
#     query_class=MarketQuery,
#     engine_options=SQLALCHEMY_ENGINE_OPTIONS,
# )
#
# cache = Cache(app, config=CACHING_OPTIONS)


def create_app(conf: str = None) -> Flask:
    # if not conf:
    #     conf = "dev" if DEV else "prod"
    #
    # if conf == "dev":
    #     db.create_all(app=app)
    #
    # if conf == "prod":
    #     app.config.update(**FLASK_PROD_CONFIG)

    warnings.filterwarnings("ignore", message="Multiple schemas resolved to the name ")
    ma = Marshmallow()
    # migrate = Migrate()

    # Marshmallow and Flask-Migrate
    ma.init_app(app)
    # migrate.init_app(app, db)

    # registering blueprints for API endpoints
    api = Api(app)
    from organizer_project.api import blueprints

    for blp in blueprints:
        api.register_blueprint(blp)

    with app.app_context():
        return app
