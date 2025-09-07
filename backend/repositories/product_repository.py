from typing import List, Optional
from models import Product

class ProductRepository:
    @staticmethod
    def get_by_id(pid: int) -> Optional[Product]:
        return Product.query.get(pid)

    @staticmethod
    def get_by_category_ids(category_ids: List[int]) -> List[Product]:
        if not category_ids:
            return []
        return Product.query.filter(Product.category_id.in_(category_ids)).all()

    @staticmethod
    def get_related(pid: int) -> List[Product]:
        p = Product.query.get(pid)
        if not p:
            return []
        # combine both directions to be safe
        return list({*p.related, *p.related_to_me})
