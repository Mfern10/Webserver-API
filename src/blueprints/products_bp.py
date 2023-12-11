from flask import Blueprint, request, jsonify
from models.product import Product, ProductSchema

products_bp = Blueprint('products_bp', __name__, url_prefix='/products')


@products_bp.route('/')
def all_products():
    products = Product.query.all()

    products_schema = ProductSchema(many=True)
    serialized_products = products_schema.dump(products)

    return jsonify(serialized_products), 200

