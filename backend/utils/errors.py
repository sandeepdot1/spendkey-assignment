from flask import jsonify

class ApiError(Exception):
    def __init__(self, message, status_code=400, details=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}

def register_error_handlers(app):
    @app.errorhandler(ApiError)
    def handle_api_error(err: ApiError):
        resp = {"error": err.message}
        if err.details:
            resp["details"] = err.details
        return jsonify(resp), err.status_code

    @app.errorhandler(404)
    def handle_404(_):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(405)
    def handle_405(_):
        return jsonify({"error": "Method not allowed"}), 405

    @app.errorhandler(422)
    def handle_422(_):
        return jsonify({"error": "Unprocessable entity"}), 422

    @app.errorhandler(Exception)
    def handle_unexpected(e):
        # In production, avoid exposing internal details
        return jsonify({"error": "Internal server error"}), 500
