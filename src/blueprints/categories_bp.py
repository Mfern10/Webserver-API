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
    # uses query all to collect all categories from the database instead of using
    # scalar as query.all() will quickly gather all the categories
    categories = Category.query.all()

    # Serialize all the categories using marshmallow schema exluding any information not nessacery
    categories_schema = CategorySchema(many=True)
    serialized_categories = categories_schema.dump(categories)

    # Return all categories in JSOn format
    return jsonify(serialized_categories), 200

# Get specific category


@categories_bp.route('/<int:category_id>', methods=['GET'])
@jwt_required()
def get_category(category_id):
    # use stmt db.select query with scalar to select a specific category from the table,
    # as long as ID matches all details of category will be returned as no security issues.
    # if id is not in system will return a 404 error
    stmt = db.select(Category).filter_by(id=category_id)
    category = db.session.scalar(stmt)
    if category:
        return CategorySchema().dump(category)
    else:
        return {'error': 'Category not found'}, 404


@categories_bp.route('/', methods=['POST'])
@jwt_required()
def new_category():
    try:
        # set variable for information collected from user must match the category schema
        category_info = CategorySchema(exclude=['id']).load(request.json)
        # check if category already exists by using SQL query to check the database
        # category names with user input category name produce error if already exists
        existing_category = Category.query.filter_by(
            name=category_info['name']).first()
        if existing_category:
            return jsonify({'error': 'Category already exists'}, 400)
        # gather the information from user and cross check then add category to db
        category = Category(
            name=category_info['name'],
            description=category_info['description']
        )
        authorize()
        db.session.add(category)
        db.session.commit()
        # return as JSON showing the details that it has been added correctly
        return CategorySchema().dump(category), 201
    except IntegrityError:
        return jsonify({'error': 'Integrity error occured while creating category'}), 500


@categories_bp.route('/<int:category_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_category(category_id):
    category_info = CategorySchema(exclude=['id']).load(request.json)
    stmt = db.select(Category).filter_by(id=category_id)
    category = db.session.scalar(stmt)
    if category:
        authorize()
        category.name = category_info.get('name', category.name)
        category.description = category_info.get(
            'description', category.description)
        db.session.commit()
        return CategorySchema().dump(category)
    else:
        return {'error': 'Category not found'}, 401


@categories_bp.route('/<int:category_id>', methods=['DELETE'])
@jwt_required()
def delete_category(category_id):
    stmt = db.select(Category).filter_by(id=category_id)
    category = db.session.scalar(stmt)
    if category:
        authorize()
        db.session.delete(category)
        db.session.commit()
        return ({'message': 'Category deleted successfully'})
    else:
        return {'error': 'Category not found'}, 404
