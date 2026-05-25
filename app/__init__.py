from flask import Flask


def create_app():
    """
    Application factory function.
    Creates and configures the Flask application instance.
    Returns the configured app object.
    """
    app = Flask(__name__)

    from app.routes import main
    app.register_blueprint(main)

    return app