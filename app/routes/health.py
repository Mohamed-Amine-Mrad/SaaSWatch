from flask import Blueprint, jsonify

from app.services.health_service import check_dependencies

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health():
    dependencies = check_dependencies()

    all_healthy = all(
        status == "up"
        for status in dependencies.values()
    )

    return jsonify({
        "status": "healthy" if all_healthy else "degraded",
        "service": "saaswatch-api",
        "dependencies": dependencies
    }), 200 if all_healthy else 503
