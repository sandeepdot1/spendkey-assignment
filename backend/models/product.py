# backend/models/product.py
from extensions import db

# association table for related products graph (bidirectional-like)
product_related = db.Table(
    "product_related",
    db.Column("product_id", db.Integer, db.ForeignKey("Product.id"), primary_key=True),
    db.Column("related_id", db.Integer, db.ForeignKey("Product.id"), primary_key=True),
)

class Product(db.Model):
    """
    Matches schema:
    CREATE TABLE Product (
      id INT PRIMARY KEY,
      name VARCHAR(255),
      price DECIMAL(10, 2),
      availability_qty INT,
      category_id INT,
      FOREIGN KEY (category_id) REFERENCES Category(id)
    );
    """
    __tablename__ = "Product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    availability_qty = db.Column(db.Integer, nullable=False, default=0)

    category_id = db.Column(db.Integer, db.ForeignKey("Category.id"), nullable=False)
    category = db.relationship("Category", backref="products")

    # related products (graph). Use symmetric/combined retrieval in repository/service if required.
    related = db.relationship(
        "Product",
        secondary=product_related,
        primaryjoin=id == product_related.c.product_id,
        secondaryjoin=id == product_related.c.related_id,
        backref="related_to_me",
    )

    def __repr__(self):
        return f"<Product {self.id}:{self.name} price={self.price} qty={self.availability_qty}>"
