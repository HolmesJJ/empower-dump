import hashlib
import pymongo

from datetime import datetime
from datetime import timedelta
from bson.objectid import ObjectId
from flask import Flask
from flask import request
from flask_cors import CORS
from flask_restful import Api
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

CONFIG = {
    "HOST": "127.0.0.1",
    "PORT": 27017,
    "DATABASE": "empower-auth",
    "CORS_HEADERS": "Content-Type",
    "CORS_RESOURCES": {r"/api/*": {"origins": "*"}},
    "JWT_SECRET_KEY": "empower-dump",
    "JWT_ACCESS_TOKEN_EXPIRE_SECONDS": 60 * 60 * 24,
    "JWT_REFRESH_TOKEN_EXPIRES_SECONDS": 60 * 60 * 24 * 30,
    "PROPAGATE_EXCEPTIONS": True
}

application = Flask(__name__, static_url_path="", static_folder="web")
application.config["CORS_HEADERS"] = CONFIG["CORS_HEADERS"]
application.config["CORS_RESOURCES"] = CONFIG["CORS_RESOURCES"]
application.config["JWT_SECRET_KEY"] = CONFIG["JWT_SECRET_KEY"]
application.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=CONFIG["JWT_ACCESS_TOKEN_EXPIRE_SECONDS"])
application.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(seconds=CONFIG["JWT_REFRESH_TOKEN_EXPIRES_SECONDS"])
application.config["PROPAGATE_EXCEPTIONS"] = CONFIG["PROPAGATE_EXCEPTIONS"]
cors = CORS(application)
api = Api(application)
jwt = JWTManager(application)

client = pymongo.MongoClient(CONFIG["HOST"], CONFIG["PORT"])
database = client[CONFIG["DATABASE"]]


class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        response = {
            "code": 1,
            "message": "success"
        }
        token = {
            "access": create_access_token(identity=identity)
        }
        response["token"] = token
        return response


class Login(Resource):
    def post(self):
        content = request.json
        response = {
            "code": 0,
            "message": ""
        }
        if "username" not in content or "password" not in content:
            response["message"] = "Missing parameters"
            return response
        username = content["username"]
        password = hashlib.sha256(content["password"].encode("utf-8")).hexdigest()
        data = list(database.patient.find({
            "username": username,
            "password": password
        }).limit(1))
        if len(data) > 0:
            token = {
                "access": create_access_token(identity="user"),
                "refresh": create_refresh_token(identity="user"),
                "type": "bearer",
                "expires_in": CONFIG["JWT_ACCESS_TOKEN_EXPIRE_SECONDS"],
            }
            response["code"] = 1
            response["message"] = "success"
            response["data"] = {
                "id": str(data[0]["_id"]),
                "username": data[0]["username"],
                "email": data[0]["email"],
                "first_name": data[0]["first_name"],
                "roles": data[0]["roles"],
                "avatar": data[0]["avatar"],
                "gender": data[0]["gender"],
                "age": data[0]["age"],
                "trial_id": data[0]["trial_id"],
                "is_control": data[0]["is_control"],
                "location": data[0]["location"]
            }
            response["token"] = token
        return response


class Summary(Resource):
    @jwt_required()
    def post(self):
        content = request.json
        response = {
            "code": 0,
            "message": ""
        }
        if "id" not in content or "date" not in content:
            response["message"] = "Missing parameters"
            return response
        patient_id = content["id"]
        date = content["date"]
        try:
            date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            response["message"] = "Error date format"
            return response
        data = list(database.daily_activity_summary.find({
            "patient": ObjectId(patient_id),
            "date": date
        }).limit(1))
        if len(data) > 0:
            response["code"] = 1
            response["message"] = "success"
            response["data"] = {
                "steps": data[0]["steps"],
                "distance": data[0]["distance"],
                "calories": data[0]["calories"],
                "active_minutes": data[0]["duration"]
            }
        return response


class Rank(Resource):
    @jwt_required()
    def get(self):
        response = {
            "code": 1,
            "message": "success"
        }
        data = database.daily_activity_summary.aggregate([
            {
                "$lookup": {
                    "from": "patient",
                    "localField": "patient",
                    "foreignField": "_id",
                    "as": "p"
                }
            },
            {
                "$group": {
                    "_id": "$patient",
                    "total_steps": {"$sum": "$steps"},
                    "username": {"$first": "$p.username"}
                }
            },
            {
                "$sort": {"total_steps": -1}
            },
            {
                "$project": {
                    "_id": False,
                    "total_steps": True,
                    "username": {"$first": "$username"}
                }
            },
        ])
        response["data"] = [item["username"] for item in data]
        return response


@jwt.unauthorized_loader
def handle_unauthorized(error):
    response = {
        "code": 0,
        "message": "Please login"
    }
    return response, 401


@jwt.invalid_token_loader
def handle_invalid_token(error):
    response = {
        "code": 0,
        "message": "Token is invalid"
    }
    return response, 401


@jwt.expired_token_loader
def handle_expired_token(header, payload):
    response = {
        "code": 0,
        "message": "Token is expired"
    }
    return response, 401


api.add_resource(Refresh, "/api/refresh", endpoint="refresh")
api.add_resource(Login, "/api/login", endpoint="login")
api.add_resource(Summary, "/api/summary", endpoint="summary")
api.add_resource(Rank, "/api/rank", endpoint="rank")


if __name__ == "__main__":
    # application.debug = True
    # application.run(host="0.0.0.0", port=5000)
    application.run()
