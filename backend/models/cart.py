# backend/models/cart.py
from extensions import db

class Cart(db.Model):
    """
    Matches schema:
    CREATE TABLE Cart (
      id INT PRIMARY KEY AUTO_INCREMENT,
      user_id INT,
      product_id INT,
      quantity INT,
      FOREIGN KEY (product_id) REFERENCES Product(id)
    );
    This table stores one row per (user_id, product_id).
    """
    __tablename__ = "Cart"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey("Product.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    product = db.relationship("Product")

    __table_args__ = (
        db.UniqueConstraint("user_id", "product_id", name="uq_cart_user_product"),
    )

    def __repr__(self):
        return f"<Cart id={self.id} user={self.user_id} product={self.product_id} qty={self.quantity}>"
