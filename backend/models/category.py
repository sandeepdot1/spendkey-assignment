# backend/models/category.py
from extensions import db

class Category(db.Model):
    """
    Matches schema:
    CREATE TABLE Category (
      id INT PRIMARY KEY,
      name VARCHAR(255),
      parent_id INT NULL,
      FOREIGN KEY (parent_id) REFERENCES Category(id)
    );
    """
    __tablename__ = "Category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey("Category.id"), nullable=True)

    # Self-referential parent/children relationship (arbitrary depth)
    parent = db.relationship(
        "Category",
        remote_side=[id],
        backref=db.backref("children", cascade="all, delete-orphan")
    )

    def __repr__(self):
        return f"<Category {self.id}:{self.name}>"
