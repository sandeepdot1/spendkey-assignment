# backend/services/cart_service.py
from typing import Dict, List
from extensions import db
from utils.errors import ApiError
from repositories.cart_repository import CartRepository
from repositories.product_repository import ProductRepository
from models import Product

class CartService:
    """
    CartService implements business logic for add, view and set-quantity
    while ensuring product availability is updated correctly.
    Uses the single-table Cart with rows per (user_id, product_id).
    """

    DEFAULT_USER_ID = 0  # guest id

    @staticmethod
    def _ensure_user(user_id) -> int:
        if user_id is None:
            return CartService.DEFAULT_USER_ID
        # accept ints or numeric strings
        try:
            uid = int(user_id)
        except (TypeError, ValueError):
            raise ApiError("userId must be an integer", 400)
        if uid < 0:
            raise ApiError("userId must be >= 0", 400)
        return uid

    @staticmethod
    def add_to_cart(product_id: int, quantity: int, user_id=None) -> Dict:
        if quantity <= 0:
            raise ApiError("quantity must be > 0", 400)

        uid = CartService._ensure_user(user_id)

        # product fetch
        product: Product = ProductRepository.get_by_id(product_id)
        if not product:
            raise ApiError("Product not found", 404)

        # determine how many items we need to deduct from stock
        existing = CartRepository.get_item(uid, product_id)
        delta = quantity  # add request means we need quantity more
        if product.availability_qty < delta:
            raise ApiError("Insufficient stock", 400)

        # Apply changes within one DB transaction (session)
        try:
            # reduce stock
            product.availability_qty = product.availability_qty - delta

            # update/create cart row
            item = CartRepository.add_or_increment_item(uid, product_id, quantity)

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ApiError("Failed to add to cart", 500)

        return {"message": "added", "userId": uid, "productId": product_id, "quantity": item.quantity}

    @staticmethod
    def get_cart(user_id=None) -> Dict:
        uid = CartService._ensure_user(user_id)
        items = CartRepository.get_items_by_user(uid)
        out_items = []
        total = 0.0
        for it in items:
            # product relationship present via Cart.product
            if not it.product:
                # skip orphaned entries (shouldn't normally happen)
                continue
            line_total = float(it.product.price) * it.quantity
            total += line_total
            out_items.append({
                "productId": it.product.id,
                "name": it.product.name,
                "unitPrice": float(it.product.price),
                "quantity": it.quantity,
                "lineTotal": round(line_total, 2)
            })
        return {"userId": uid, "items": out_items, "total": round(total, 2)}

    @staticmethod
    def set_quantity(product_id: int, quantity: int, user_id=None) -> Dict:
        if quantity < 0:
            raise ApiError("quantity must be >= 0", 400)

        uid = CartService._ensure_user(user_id)

        product: Product = ProductRepository.get_by_id(product_id)
        if not product:
            raise ApiError("Product not found", 404)

        existing = CartRepository.get_item(uid, product_id)
        old_qty = existing.quantity if existing else 0
        delta = quantity - old_qty  # positive => need more stock, negative => release stock

        # If increasing quantity, check stock
        if delta > 0 and product.availability_qty < delta:
            raise ApiError("Insufficient stock to increase quantity", 400)

        try:
            # adjust stock
            product.availability_qty = product.availability_qty - delta

            # update cart row (set or delete)
            item = CartRepository.set_item_quantity(uid, product_id, quantity)

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ApiError("Failed to set quantity", 500)

        return {"message": "updated", "productId": product_id, "quantity": (item.quantity if item else 0)}
