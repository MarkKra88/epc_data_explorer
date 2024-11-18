from flask import Flask

def create_app() -> Flask:
    """Factory function to create the Flask app."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure key

    # Import and register routes
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
