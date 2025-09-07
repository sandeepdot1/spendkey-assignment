from flask import Flask, jsonify
from config import Config
from extensions import db, ma
from utils.errors import register_error_handlers
from controllers.category_controller import category_bp
from controllers.product_controller import product_bp
from controllers.cart_controller import cart_bp
from flask_cors import CORS  # <-- add this


def create_app(config_obj: type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_obj)

    # Enable CORS for all routes
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Extensions
    db.init_app(app)
    ma.init_app(app)

    # Blueprints
    app.register_blueprint(category_bp, url_prefix="/")
    app.register_blueprint(product_bp, url_prefix="/")
    app.register_blueprint(cart_bp, url_prefix="/")

    # Errors
    register_error_handlers(app)

    # Health
    @app.get("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
