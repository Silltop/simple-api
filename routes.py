from flask import jsonify
from api import app
from flask import Blueprint, request
import db_ops
from geolocation import geolocation_factory
from validators import *

v1 = Blueprint("v1", __name__, url_prefix="/v1")
geolocation_controller = geolocation_factory.GeolocationApiFactory()


@app.route("/", methods=["GET"])
def index():
    abort(404, "Wrong path, please use /v1/endpoint")


@v1.route("", methods=["GET"])
def api_index():
    result = {"Info": "This is v1 api response, please use /v1/geolocate endpoint, GET or POST for batch response"}
    return jsonify(result), 200


# Assuming that the operations should be done in bulk


@v1.route("/geolocation/add", methods=["POST"])
def add():
    request_data = request.get_json()
    ips = []
    ips_to_check = request_data.get("ips", [])
    domains = request_data.get("domains", [])
    ips = [ip for ip in ips_to_check if is_valid_ip(ip)]
    ips.extend([dns_resolve_ip(domain) for domain in domains if is_valid_url(domain)])
    result = geolocation_controller.batch_geolocate(ips)
    db_ops.add_results_to_db(result)
    return jsonify(result), 200


@v1.route("/geolocation/delete", methods=["DELETE"])
def delete():
    db_ops.delete_result_from_db(request.get_json().get("ips", []))
    return jsonify({"status": "ok"}), 200


@v1.route("/geolocation/get", methods=["GET", "POST"])
def get():
    if request.method == "GET":
        ip = request.args.get("ip", [])
        return jsonify(db_ops.get_results_from_db([ip])), 200
    elif request.method == "POST":
        request_data = request.get_json()
        db_data = db_ops.get_results_from_db(request_data.get("ips", []))
        return jsonify(db_data), 200
    else:
        abort(405, "Method not allowed")
