from flask import Blueprint, request, jsonify
from models.product import Product, ProductSchema
from setup import db
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity

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

  









# @products_bp.route('/', methods=['POST'])
# # @jwt_required()
# # def new_product():
# #     try:
# #         current_user_id = get_jwt_identity()
# #         # set variable for information collected from user must match the Product schema
# #         product_info = ProductSchema(exclude=['id']).load(request.json)
# #         # check if Product already exists by using SQL query to check the database 
# #         #product names with user input product name produce error if already exists
# #         existing_product = Product.query.filter_by(name=product_info['name']).first()
# #         if existing_product:
# #             return jsonify({'error': 'Category already exists'}, 400)
# #         # gather the information from user and cross check then add category to db
# #         product = Product(
# #             name = product_info['name'],
# #             description = product_info['description'],
# #             price = product_info['price'],
# #             color = product_info['color'],
# #             user_id = current_user_id,
# #             category_id = product_info['category_id']
# #         )
        
# #         db.session.add(product)
# #         db.session.commit()
# #         # return as JSON showing the details that it has been added correctly
# #         return ProductSchema().dump(product), 201
# #     except IntegrityError:
#         return jsonify({'error': 'Integrity error occured while creating product'}), 500
    
# @categories_bp.route('/<int:category_id>', methods=['PUT', 'PATCH'])
# @jwt_required()
# def update_category(category_id):
#     category_info = CategorySchema(exclude=['id']).load(request.json)
#     stmt = db.select(Category).filter_by(id=category_id)
#     category = db.session.scalar(stmt)
#     if category:
#         authorize()
#         category.name = category_info.get('name', category.name)
#         category.description = category_info.get('description', category.description)
#         db.session.commit()
#         return CategorySchema().dump(category)
#     else:
#         return {'error': 'Category not found'}, 401

# @categories_bp.route('/<int:category_id>', methods=['DELETE'])
# @jwt_required()
# def delete_category(category_id):
#         stmt = db.select(Category).filter_by(id=category_id)
#         category = db.session.scalar(stmt)
#         if category:
#             authorize()
#             db.session.delete(category)
#             db.session.commit()
#             return ({'message': 'Category deleted successfully'})
#         else:
#             return {'error': 'Category not found'}, 404

