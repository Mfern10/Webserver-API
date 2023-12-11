from flask import Blueprint, request, jsonify
from models.product import Product, ProductSchema
from setup import db
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth import authorize

products_bp = Blueprint('products_bp', __name__, url_prefix='/products')

# Get all products
@products_bp.route('/', methods=['GET'])
def all_products():
    products = Product.query.all()

    products_schema = ProductSchema(many=True)
    serialized_products = products_schema.dump(products)

    return jsonify(serialized_products), 200

@products_bp.route('/<int:product_id>', methods = ['GET'])

def get_product(product_id):
    # use stmt db.select query with scalar to select a specific category from the table,
    # as long as ID matches all details of category will be returned as no security issues.
    # if id is not in system will return a 404 error
    stmt = db.select(Product).filter_by(id=product_id)
    category = db.session.scalar(stmt)
    if category:
        return ProductSchema().dump(category)
    else:
        return {'error': 'Product not found'}, 404
    



from datetime import datetime

@products_bp.route('/', methods=['POST'])
@jwt_required()
def new_product():
    try:
        current_user_id = get_jwt_identity()
        product_info = ProductSchema(exclude=['id']).load(request.json)
        
        existing_product = Product.query.filter_by(name=product_info['name']).first()
        if existing_product:
            return jsonify({'error': 'Product already exists'}), 400
        
        product = Product(
            name=product_info['name'],
            description=product_info['description'],
            price=product_info['price'],
            color=product_info['color'],
            user_id=current_user_id,
            category_id=product_info['category_id'],
            date_created=datetime.now()  # Set date_created to the current timestamp
        )
        
        db.session.add(product)
        db.session.commit()
        
        return ProductSchema().dump(product), 201
    except IntegrityError:
        return jsonify({'error': 'Integrity error occured while creating product'}), 500

  
@products_bp.route('/<int:product_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_product(product_id):
    product_info = ProductSchema(exclude=['id','user_id', 'date_created']).load(request.json)
    stmt = db.select(Product).filter_by(id=product_id)
    product = db.session.scalar(stmt)
    if product:
        authorize(product.user_id)
        product.name = product_info.get('name', product.name)
        product.description = product_info.get('description', product.description)
        product.price = product_info.get('price', product.price)
        product.color = product_info.get('color', product.color)
        product.category_id = product_info.get('category_id', product.category_id)
        db.session.commit()
        return ProductSchema().dump(product)
    else:
        return {'error': 'Product not found'}, 401

@products_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
        stmt = db.select(Product).filter_by(id=product_id)
        product = db.session.scalar(stmt)
        if product:
            authorize()
            db.session.delete(product)
            db.session.commit()
            return ({'message': 'Product deleted successfully'}), 200
        else:
            return {'error': 'Product not found'}, 404

