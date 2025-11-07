from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()


def create_app(config_object=None):
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_mapping(
        SECRET_KEY="dev-secret",
        SQLALCHEMY_DATABASE_URI="sqlite:///elearn.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY="jwt-secret",
    )

    if config_object:
        app.config.from_object(config_object)

    db.init_app(app)
    jwt.init_app(app)

    # import routes to register them
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app
