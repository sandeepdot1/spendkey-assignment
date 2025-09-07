# backend/repositories/cart_repository.py
from typing import List, Optional
from extensions import db
from models import Cart

class CartRepository:
    @staticmethod
    def get_items_by_user(user_id: int) -> List[Cart]:
        return Cart.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_item(user_id: int, product_id: int) -> Optional[Cart]:
        return Cart.query.filter_by(user_id=user_id, product_id=product_id).first()

    @staticmethod
    def add_or_increment_item(user_id: int, product_id: int, quantity: int) -> Cart:
        """
        Adds or increments the cart row for (user_id, product_id).
        NOTE: This method does NOT commit — caller (service) should commit so that stock changes and cart changes happen atomically.
        """
        item = CartRepository.get_item(user_id, product_id)
        if item:
            item.quantity += quantity
        else:
            item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
            db.session.add(item)
        return item

    @staticmethod
    def set_item_quantity(user_id: int, product_id: int, quantity: int) -> Optional[Cart]:
        """
        Sets the quantity to a value. If quantity == 0, it will delete the row.
        NOTE: Does NOT commit; caller should commit.
        """
        item = CartRepository.get_item(user_id, product_id)
        if item:
            if quantity <= 0:
                db.session.delete(item)
                return None
            item.quantity = quantity
            return item
        else:
            if quantity <= 0:
                return None
            item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
            db.session.add(item)
            return item

    @staticmethod
    def delete_item(user_id: int, product_id: int) -> None:
        item = CartRepository.get_item(user_id, product_id)
        if item:
            db.session.delete(item)
