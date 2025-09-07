# backend/seed.py
"""
Seed the database with a sample category tree, products, and related links.

Run:
  cd backend
  python seed.py
"""
from app import create_app
from extensions import db
from models import Category, Product, Cart

def ensure_bidirectional_related(p1: Product, p2: Product):
    if p2 not in p1.related:
        p1.related.append(p2)
    if p1 not in p2.related:
        p2.related.append(p1)

def run():
    app = create_app()
    with app.app_context():
        # drop/create for fresh seed
        db.drop_all()
        db.create_all()

        # Categories
        electronics = Category(name="Electronics")
        computers = Category(name="Computers", parent=electronics)
        laptops = Category(name="Laptops", parent=computers)
        desktops = Category(name="Desktops", parent=computers)
        phones = Category(name="Phones", parent=electronics)

        fashion = Category(name="Fashion")
        men = Category(name="Men", parent=fashion)
        women = Category(name="Women", parent=fashion)

        db.session.add_all([electronics, computers, laptops, desktops, phones, fashion, men, women])
        db.session.flush()

        # Products (with availability_qty)
        p1 = Product(name='Ultrabook 13"', price=999.99, availability_qty=10, category=laptops)
        p2 = Product(name='Gaming Laptop 15"', price=1599.50, availability_qty=5, category=laptops)
        p3 = Product(name='Workstation Desktop', price=1899.00, availability_qty=3, category=desktops)
        p4 = Product(name='Flagship Phone X', price=799.00, availability_qty=8, category=phones)
        p5 = Product(name='Budget Phone A', price=299.00, availability_qty=20, category=phones)
        p6 = Product(name="Men's Sneakers", price=79.99, availability_qty=25, category=men)
        p7 = Product(name="Women's Jacket", price=129.99, availability_qty=12, category=women)

        db.session.add_all([p1, p2, p3, p4, p5, p6, p7])
        db.session.flush()

        # Related graph (bidirectional)
        ensure_bidirectional_related(p1, p2)
        ensure_bidirectional_related(p4, p5)
        ensure_bidirectional_related(p2, p3)

        # Optional: add sample cart rows (user_id is integer)
        # For example user 1 has 1 unit of product 1
        sample_cart = Cart(user_id=1, product_id=p1.id, quantity=1)
        db.session.add(sample_cart)

        db.session.commit()
        print("Seed complete.")

if __name__ == "__main__":
    run()
