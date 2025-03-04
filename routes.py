from flask import jsonify
from api import app
from flask import Blueprint

v1 = Blueprint("v1", __name__, url_prefix="/v1")


@app.route("/", methods=["GET"])
def index():
    result = {"Error": "Wrong path, please use /v1/endpoint"}
    return jsonify(result), 404


@v1.route("", methods=["GET"])
def api_index():
    result = {"Welcome": "This is v1 api response"}
    return jsonify(result), 200
