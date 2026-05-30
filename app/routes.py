from flask import Blueprint, jsonify, send_from_directory
import os
import time
import platform

main = Blueprint('main', __name__)

# Record the time the app started
START_TIME = time.time()


@main.route('/', methods=['GET'])
def home():
    return send_from_directory(
        os.path.join(os.path.dirname(__file__), 'static'),
        'index.html'
    )


@main.route('/health', methods=['GET'])
def health_check():
    """
    Enhanced health check endpoint.
    Returns app status, uptime, and system information.
    Used by monitoring scripts and CI/CD pipeline to verify deployment.
    """
    uptime_seconds = int(time.time() - START_TIME)
    uptime_minutes = uptime_seconds // 60
    uptime_hours   = uptime_minutes // 60

    return jsonify({
        "status":   "healthy",
        "service":  "devops-project",
        "version":  "1.0.0",
        "uptime": {
            "seconds": uptime_seconds,
            "minutes": uptime_minutes,
            "hours":   uptime_hours
        },
        "system": {
            "python":   platform.python_version(),
            "platform": platform.system(),
            "node":     platform.node()
        }
    }), 200


@main.route('/status', methods=['GET'])
def status():
    """
    Simple status endpoint for quick checks.
    Returns minimal response for fast monitoring checks.
    """
    return jsonify({"ok": True}), 200