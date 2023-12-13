from datetime import datetime
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
    # Retrieving all prducts from the database
    products = Product.query.all()

    # Serializing the products with ProductSchema
    products_schema = ProductSchema(many=True)
    serialized_products = products_schema.dump(products)

    # Returns the list of products as JSON
    return jsonify(serialized_products), 200


@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    # Select query for specific product by ID
    stmt = db.select(Product).filter_by(id=product_id)
    product = db.session.scalar(stmt)

    # Handling the retrieved product data
    if product:
        # Serialize the retrieved product using ProductSchema
        # Return as JSON
        return ProductSchema().dump(product)
    else:
        # Returning 404 if product not found
        return {'error': 'Product not found'}, 404


@products_bp.route('/', methods=['POST'])
@jwt_required()
def new_product():
    try:
        # obtaining the current users identity from JWT
        current_user_id = get_jwt_identity()

        # Loads and validates the user provided data with ProductSchema
        product_info = ProductSchema(exclude=['id']).load(request.json)

        # Check if the product with the same name already exists
        existing_product = Product.query.filter_by(
            name=product_info['name']).first()
        if existing_product:
            return jsonify({'error': 'Product already exists'}), 400

        # Creating a a new product object  using user provided data
        product = Product(
            name=product_info['name'],
            description=product_info['description'],
            price=product_info['price'],
            color=product_info['color'],
            user_id=current_user_id,
            category_id=product_info['category_id'],
            date_created=datetime.now()  # Set date_created to the current timestamp
        )

        # Adding new product to the database
        db.session.add(product)
        db.session.commit()

        # Returns newly created product as JSON
        return ProductSchema().dump(product), 201

    # Shows Integreity 500 if error occurs
    except IntegrityError:
        return jsonify({'error': 'Integrity error occured while creating product'}), 500


@products_bp.route('/<int:product_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_product(product_id):
    # Loading and validating the user provided data using ProductSchema
    product_info = ProductSchema(
        exclude=['id', 'user_id', 'date_created'], partial=True).load(request.json)

    # Uses Selecy to query the specific product by its ID
    stmt = db.select(Product).filter_by(id=product_id)
    product = db.session.scalar(stmt)

    # Handling the retrived product data
    if product:
        authorize(product.user_id)

        # Updating the product details if they are provided in the request,
        # Else keep existing values
        product.name = product_info.get('name', product.name)
        product.description = product_info.get(
            'description', product.description)
        product.price = product_info.get('price', product.price)
        product.color = product_info.get('color', product.color)
        product.category_id = product_info.get(
            'category_id', product.category_id)

        # Commiting the changes to the product to the database
        db.session.commit()

        # Returns the updated product details as JSON
        return ProductSchema().dump(product)
    else:
        # Returns 401 if ID does not exist
        return {'error': 'Product not found'}, 404


@products_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    # Select query to get the specific product by its ID
    stmt = db.select(Product).filter_by(id=product_id)
    product = db.session.scalar(stmt)

    # Handling the Retrieved data
    if product:
        authorize()  # Autorizes the delete action if logic met

        # Delete the product and commit to the database
        db.session.delete(product)
        db.session.commit()

        # Returning a message indicating successful delete
        return ({'message': 'Product deleted successfully'}), 200
    else:
        # Returns error 404 if ID does not exist
        return {'error': 'Product not found'}, 404
