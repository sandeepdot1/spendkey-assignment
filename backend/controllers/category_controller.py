from flask import Blueprint, jsonify

from services.category_service import CategoryService

category_bp = Blueprint("categories", __name__)

@category_bp.get("/categories")
def get_categories():
    tree = CategoryService.get_full_tree()
    return jsonify(tree), 200
