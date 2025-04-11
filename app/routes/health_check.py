from flask import Blueprint, request, make_response
from app.services.health_check_service import insert_health_check
from app.utils.logger import log_request, webapp_logger
from datetime import datetime
import time
from app.utils.statsd_client import increment_counter, record_timer

health_check_blueprint = Blueprint("health_check", __name__)

@health_check_blueprint.route("/healthz", methods=["GET"],provide_automatic_options=False)
@log_request
def health_check():
    start_time = time.time()
    increment_counter("api.get.calls")
    if request.method != "GET":
        return make_response("", 405)
    if request.data or request.files:
        return make_response("", 400)  # Bad Request

    # Insert record
    if insert_health_check():
        response = make_response("", 200)
    else:
        response = make_response("", 503)  # Service Unavailable

        webapp_logger.info("Health check performed")

@health_check_blueprint.route("/cicd", methods=["GET"],provide_automatic_options=False)
@log_request
def health_check():
    start_time = time.time()
    increment_counter("api.get.calls")
    if request.method != "GET":
        return make_response("", 405)
    if request.data or request.files:
        return make_response("", 400)  # Bad Request

    # Insert record
    if insert_health_check():
        response = make_response("", 200)
    else:
        response = make_response("", 503)  # Service Unavailable

        webapp_logger.info("Health check performed")


    # Add headers
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate;"
    response.headers["Pragma"] = "no-cache"
    response.headers["X-Content-Type-Options"] = "nosniff"

    duration = time.time() - start_time
    record_timer("api.get_call.duration", duration) 

    

    return response

@health_check_blueprint.route("/healthz", methods=["HEAD","OPTIONS","POST", "PUT", "DELETE", "PATCH"])
@log_request
def method_not_allowed():
    return make_response("", 405)  # Method Not Allowed