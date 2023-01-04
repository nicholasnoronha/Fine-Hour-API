import os

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from db import db
# from blocklist import BLOCKLIST #! need column 'insert only'
import models #!
from models import BlocklistModel

from resources.user import blp as UserBlueprint
from resources.task import blp as TaskBlueprint

def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()

    app.config["PROPAGATE_EXCEPTIONS"] = True 

    app.config["API_TITLE"] = "Fine Hour API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3" 
    app.config["OPENAPI_URL_PREFIX"] = "/"

    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)
    api = Api(app)

    app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY", "testtest")
    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]

        try:
            blocklist_token = BlocklistModel.query.filter(BlocklistModel.token_jti == jti).first()
            if not blocklist_token:
                return False
            else:
                if blocklist_token.token_jti == jti:
                    return True
                else:
                    return False
        except:
            return {"error": "Something went wrong."}

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return(
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            )
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return(
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required"
                },
                401
            )
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required"
                },
                401
            )
        )

    api.register_blueprint(UserBlueprint)
    api.register_blueprint(TaskBlueprint)
    
    return app