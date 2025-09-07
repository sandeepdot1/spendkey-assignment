from typing import List, Optional
from extensions import db
from models import Category

class CategoryRepository:
    @staticmethod
    def get_all() -> List[Category]:
        return Category.query.all()

    @staticmethod
    def get_by_id(category_id: int) -> Optional[Category]:
        return Category.query.get(category_id)

    @staticmethod
    def get_children(category_id: int) -> List[Category]:
        return Category.query.filter_by(parent_id=category_id).all()

    @staticmethod
    def add(category: Category):
        db.session.add(category)
        db.session.commit()
