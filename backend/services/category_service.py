from typing import Dict, List
from repositories.category_repository import CategoryRepository
from utils.errors import ApiError
from models import Category

class CategoryService:
    @staticmethod
    def _build_tree(node: Category) -> Dict:
        return {
            "id": node.id,
            "name": node.name,
            "children": [CategoryService._build_tree(child) for child in node.children]
        }

    @staticmethod
    def get_full_tree() -> List[Dict]:
        # roots are categories without parent
        roots = [c for c in CategoryRepository.get_all() if c.parent_id is None]
        return [CategoryService._build_tree(root) for root in roots]

    @staticmethod
    def get_descendant_ids(category_id: int) -> List[int]:
        start = CategoryRepository.get_by_id(category_id)
        if not start:
            raise ApiError("Category not found", 404)

        ids = []

        def dfs(c: Category):
            ids.append(c.id)
            for ch in c.children:
                dfs(ch)

        dfs(start)
        return ids
