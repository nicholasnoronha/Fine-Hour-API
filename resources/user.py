from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from db import db
# from blocklist import BLOCKLIST
from models import UserModel
from models import BlocklistModel
from schemas import UserSchema
from schemas import JtiSchema

blp = Blueprint("Users", __name__, description="Operations on users.")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.email == user_data["email"]).first():
            abort(409, message="A user with that email already exists.")

        user = UserModel(
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully."}, 201

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.email == user_data["email"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}
        abort(401, message="Invalid credentials.")

@blp.route("/logout")
class user_logout(MethodView):
    @jwt_required()
    def post(self):
        temp_jti = {"token_jti": get_jwt()["jti"]}
        jti = BlocklistModel(**temp_jti)
        try:
            db.session.add(jti)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the jti into the database.")
        
        return {"message": "Successfully logged out."}

@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}

@blp.route("/user/<string:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

@blp.route("/ok")
class User(MethodView):
    @jwt_required()
    @blp.response(200, JtiSchema(many=True))
    def get(self):
        jti = BlocklistModel.query.all()
        # jti = get_jwt()["jti"]

        # print("JTIJTIJTI", jti)
        # try:
        #     blocklist_token = BlocklistModel.query.filter(jti=jti).first()
        #     print("bloblblobobl",blocklist_token.jti)
        #     if blocklist_token.jti == jti:
        #         return {"message": "True"}
        #     else:
        #         return {"message": "False"}
        # except:
        #     return {"erro": "erro"}
        return jti

@blp.route("/pok")
class User(MethodView):
    @jwt_required()
    # @blp.response(200, JtiSchema)
    def get(self):
        jti = get_jwt()["jti"]

        try:
            print("AAAA")
            blocklist_token = BlocklistModel.query.filter(BlocklistModel.token_jti == jti).first()
            print("bbbb", blocklist_token)
            if not blocklist_token:
                return "False"
            else:
                if blocklist_token.token_jti == jti:
                    print("cccc")
                    return {"message": "True"}
                else:
                    print("dddd")
                    return {"message": "False"}
        except:
            return {"error": "Something went wrong."}