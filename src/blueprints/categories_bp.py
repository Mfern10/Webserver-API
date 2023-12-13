from setup import db
from flask import Blueprint, jsonify, request
from models.category import Category, CategorySchema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required
from auth import authorize


categories_bp = Blueprint('categories_bp', __name__, url_prefix='/categories')

# View list of categories


@categories_bp.route('/', methods=['GET'])
@jwt_required()
def all_categories():
    # Retrieving all categories from the database
    categories = Category.query.all()

    # Serializing all categories using CategorySchema
    serialized_categories = CategorySchema(many=True).dump(categories)

    # Returning all categories as JSON
    return serialized_categories, 200

# Get specific category


@categories_bp.route('/<int:category_id>', methods=['GET'])
@jwt_required()
def get_category(category_id):
    # Querying a specific category from the database by ID
    stmt = db.select(Category).filter_by(id=category_id)
    category = db.session.scalar(stmt)

    # Handling the retrieved category data
    if category:
        # Serializing the retrieved category using CategorySchema
        serialized_category = CategorySchema().dump(category)
        return serialized_category, 200  # Returning the serialized category
    else:
        # Returning a 404 error if category not found
        return {'error': 'Category not found'}, 404


@categories_bp.route('/', methods=['POST'])
@jwt_required()
def new_category():
    try:
        # Loading and validating user-provided data using CategorySchema
        category_info = CategorySchema(exclude=['id']).load(request.json)

        # Checking if the category already exists in the database
        existing_category = Category.query.filter_by(
            name=category_info['name']).first()
        if existing_category:
            return jsonify({'error': 'Category already exists'}, 400)

        # Creating a new category and adding it to the database
        category = Category(
            name=category_info['name'],
            description=category_info['description']
        )
        authorize()  # Authorization logic (if applicable)
        db.session.add(category)
        db.session.commit()

        # Returning the details of the added category as JSON
        return CategorySchema().dump(category), 201
    except IntegrityError:
        # Handling integrity error while creating the category
        return jsonify({'error': 'Integrity error occurred while creating category'}), 500


@categories_bp.route('/<int:category_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_category(category_id):
    # Loading user-provided data and querying the category by ID
    category_info = CategorySchema(exclude=['id'], partial=True).load(request.json)
    stmt = db.select(Category).filter_by(id=category_id)
    category = db.session.scalar(stmt)

    # Handling the retrieved category data
    if category:
        authorize()  # Authorizing the update action

        # Updating category details if provided in the request, else keeping the existing values
        category.name = category_info.get('name', category.name)
        category.description = category_info.get(
            'description', category.description)

        db.session.commit()  # Committing the changes to the database

        # Returning the updated category details as JSON
        return CategorySchema().dump(category)
    else:
        # Returning a 401 error if category is not found
        return {'error': 'Category not found'}, 401


@categories_bp.route('/<int:category_id>', methods=['DELETE'])
@jwt_required()
def delete_category(category_id):
    # Querying the category by ID
    stmt = db.select(Category).filter_by(id=category_id)
    category = db.session.scalar(stmt)

    # Handling the retrieved category data
    if category:
        authorize()  # Authorizing the delete action

        # Deleting the category from the database
        db.session.delete(category)
        db.session.commit()

        # Returning a success message upon successful deletion
        return {'message': 'Category deleted successfully'}
    else:
        # Returning a 404 error if the category is not found
        return {'error': 'Category not found'}, 404
