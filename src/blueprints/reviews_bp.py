from flask import Blueprint, request, jsonify
from setup import db
from models.review import Review, ReviewSchema 
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth import authorize
from sqlalchemy.exc import IntegrityError
from models.product import Product

reviews_bp = Blueprint('reviews_bp', __name__, url_prefix='/reviews')

@reviews_bp.route('/', methods = ['GET'])
# @jwt_required()
def all_reviews():
    # uses query all to collect all Reviews from the database instead of using
    # scalar as query.all() will quickly gather all the reviews
    reviews = Review.query.all()

    # Serialize all the reviews using marshmallow schema exluding any information not nessacery
    reviews_schema = ReviewSchema(many=True)
    serialized_reviews = reviews_schema.dump(reviews)

    # Return all categories in JSOn format
    return jsonify(serialized_reviews), 200

# # Get specific review
@reviews_bp.route('/<int:review_id>', methods = ['GET'])
# @jwt_required()
def get_review(review_id):
    # use stmt db.select query with scalar to select a specific review from the table,
    # as long as ID matches all details of review will be returned as no security issues.
    # if id is not in system will return a 404 error
    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)
    if review:
        return ReviewSchema().dump(review)
    else:
        return {'error': 'Review not found'}, 404
    
@reviews_bp.route('/', methods=['POST'])
@jwt_required()
def new_review():
    try:
        current_user_id = get_jwt_identity()
        review_info = ReviewSchema().load(request.json)  # Load entire schema
        
        # Check if the product_id exists in the database
        product_id = review_info.get('product_id')
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}, 404)
        
        # Check if the user has already reviewed the product with the same title
        existing_review = Review.query.filter_by(
            user_id=current_user_id,
            product_id=product_id,
            title=review_info.get('title')
        ).first()
        if existing_review:
            return jsonify({'error': 'You have already reviewed this product'}), 400
        
        review = Review(
            title=review_info['title'],
            message=review_info['message'],
            product_id=product_id,
            user_id=current_user_id
        )
        
        db.session.add(review)
        db.session.commit()
        
        return ReviewSchema().dump(review), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Integrity error occurred while creating review'}), 500



    
@reviews_bp.route('/<int:review_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_review(review_id):
    review_info = ReviewSchema(exclude=['id', 'product_id']).load(request.json)
    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)
    if review:
        authorize(review.user_id)
        review.title = review_info.get('title', review.title)
        review.message = review_info.get('message', review.message)
        db.session.commit()
        return ReviewSchema().dump(review)
    else:
        return {'error': 'Review not found'}, 401

@reviews_bp.route('/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
        stmt = db.select(Review).filter_by(id=review_id)
        review = db.session.scalar(stmt)
        if review:
            authorize()
            db.session.delete(review)
            db.session.commit()
            return ({'message': 'Review deleted successfully'})
        else:
            return {'error': 'Review not found'}, 404
