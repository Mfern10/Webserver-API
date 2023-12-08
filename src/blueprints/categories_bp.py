from setup import db
from flask import Blueprint, jsonify
from models.category import Category, CategorySchema


categories_bp = Blueprint('categories_bp', __name__, url_prefix='/categories')

# View list of categories 
@categories_bp.route('/', methods = ['GET'])
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
@categories_bp.route('/<int:category_id>', methods = ['GET'])
def get_category(category_id):
    stmt = db.select(Category).filter_by(id=category_id)
    category = db.session.scalar(stmt)

    if category:
        return CategorySchema().dump(category)
    else:
        return {'error': 'Category not found'}, 404
    