import warnings
from typing import TYPE_CHECKING
from flask import Flask, Response, redirect, request

# from flask_caching import Cache
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_smorest import Api
from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy


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


db = SQLAlchemy(app)

# db = SQLAlchemy(app)
#
# cache = Cache(app, config=CACHING_OPTIONS)


def create_app(conf: str = None) -> Flask:
    warnings.filterwarnings("ignore", message="Multiple schemas resolved to the name ")
    ma = Marshmallow()
    migrate = Migrate()

    # db.init_app(app)

    # Marshmallow and Flask-Migrate
    ma.init_app(app)

    with app.app_context():
        import organizer_project.models

        db.create_all()
        migrate.init_app(app, db)

    # registering blueprints for API endpoints
    api = Api(app)
    from organizer_project.api import blueprints

    for blp in blueprints:
        api.register_blueprint(blp)

    with app.app_context():
        return app
