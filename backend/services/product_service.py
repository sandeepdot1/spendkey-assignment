from typing import List, Dict
from repositories.product_repository import ProductRepository
from services.category_service import CategoryService
from utils.errors import ApiError
from models import Product

class ProductService:
    @staticmethod
    def get_products_by_category_including_descendants(category_id: int) -> List[Product]:
        category_ids = CategoryService.get_descendant_ids(category_id)
        return ProductRepository.get_by_category_ids(category_ids)

    @staticmethod
    def get_related_products(pid: int) -> List[Product]:
        products = ProductRepository.get_related(pid)
        if products is None:
            raise ApiError("Product not found", 404)
        return products

    @staticmethod
    def get_product_or_404(pid: int) -> Product:
        p = ProductRepository.get_by_id(pid)
        if not p:
            raise ApiError("Product not found", 404)
        return p
