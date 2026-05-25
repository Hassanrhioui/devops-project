from flask import Blueprint, jsonify

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def home():
    """
    Home endpoint.
    Returns a welcome message as JSON.
    """
    return jsonify({
        "message": "Hello from the DevOps project!",
        "status": "running"
    }), 200


@main.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    Used by monitoring systems to verify the app is alive.
    Returns HTTP 200 if healthy.
    """
    return jsonify({
        "status": "healthy",
        "service": "devops-project"
    }), 200