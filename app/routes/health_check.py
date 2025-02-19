from flask import Blueprint, request, make_response
from app.services.health_check_service import insert_health_check

health_check_blueprint = Blueprint("health_check", __name__)

@health_check_blueprint.route("/healthz", methods=["GET"],provide_automatic_options=False)
def health_check():
    # Disallow payload
    if request.method != "GET":
        return make_response("", 405)
    if request.data:
        return make_response("", 400)  # Bad Request

    # Insert record
    if insert_health_check():
        response = make_response("", 200)
    else:
        response = make_response("", 503)  # Service Unavailable

    # Add headers
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate;"
    response.headers["Pragma"] = "no-cache"
    response.headers["X-Content-Type-Options"] = "nosniff"

    return response

@health_check_blueprint.route("/healthz", methods=["HEAD","OPTIONS","POST", "PUT", "DELETE", "PATCH"])
def method_not_allowed():
    return make_response("", 405)  # Method Not Allowed