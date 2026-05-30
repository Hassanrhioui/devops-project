from flask import Blueprint, jsonify, send_from_directory
import os

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def home():
    return send_from_directory(
        os.path.join(os.path.dirname(__file__), 'static'),
        'index.html'
    )

@main.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "devops-project"
    }), 200