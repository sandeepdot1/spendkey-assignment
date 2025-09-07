# backend/controllers/cart_controller.py
from flask import Blueprint, request, jsonify
from utils.validators import must_be_positive_int
from services.cart_service import CartService

cart_bp = Blueprint("cart", __name__)

@cart_bp.post("/cart/add")
def add_to_cart():
    data = request.get_json(silent=True) or {}

    # productId and quantity required
    pid = data.get("productId")
    qty = data.get("quantity")

    # validate
    pid = must_be_positive_int("productId", pid)
    qty = must_be_positive_int("quantity", qty)

    user_id = data.get("userId")  # optional; CartService will default to guest id 0 if None
    result = CartService.add_to_cart(pid, qty, user_id)
    return jsonify(result), 201

@cart_bp.get("/cart")
def get_cart():
    # userId via query param optional; default handled in service
    user_id = request.args.get("userId")
    result = CartService.get_cart(user_id)
    return jsonify(result), 200

@cart_bp.post("/cart/set-quantity")
def set_quantity():
    data = request.get_json(silent=True) or {}
    pid = data.get("productId")
    if pid is None:
        return jsonify({"error": "'productId' is required"}), 400
    try:
        pid = int(pid)
        if pid <= 0:
            raise ValueError()
    except (TypeError, ValueError):
        return jsonify({"error": "'productId' must be a positive integer"}), 400

    try:
        qty = int(data.get("quantity"))
    except (TypeError, ValueError):
        return jsonify({"error": "'quantity' must be an integer >= 0"}), 400

    user_id = data.get("userId") or request.args.get("userId")
    result = CartService.set_quantity(pid, qty, user_id)
    return jsonify(result), 200
