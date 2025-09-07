from flask import Blueprint, jsonify, request
from utils.validators import must_be_positive_int
from services.product_service import ProductService

product_bp = Blueprint("products", __name__)

@product_bp.get("/products")
def get_products_for_category():
    category_id = request.args.get("categoryId")
    cid = must_be_positive_int("categoryId", category_id)
    products = ProductService.get_products_by_category_including_descendants(cid)
    out = [{"id": p.id, "name": p.name, "price": p.price, "categoryId": p.category_id, "availabilityQty": p.availability_qty} for p in products]
    
    return jsonify(out), 200

@product_bp.get("/product/<int:pid>/related")
def get_related(pid: int):
    products = ProductService.get_related_products(pid)
    out = [{"id": p.id, "name": p.name, "price": p.price, "categoryId": p.category_id} for p in products]
    
    return jsonify(out), 200
