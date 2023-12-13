from flask import Blueprint, request, jsonify
from setup import db
from models.review import Review, ReviewSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth import authorize
from sqlalchemy.exc import IntegrityError
from models.product import Product

reviews_bp = Blueprint('reviews_bp', __name__, url_prefix='/reviews')


@reviews_bp.route('/', methods=['GET'])
@jwt_required()
def all_reviews():
    # uses query all method to query all the reviews in the database
    reviews = Review.query.all()

    # Serializing all the reviews using marshmallow schema and excluding unnecessary info
    reviews_schema = ReviewSchema(many=True)
    serialized_reviews = reviews_schema.dump(reviews)

    # Return all reviews data in JSON format
    return jsonify(serialized_reviews), 200

# Get specific review


@reviews_bp.route('/<int:review_id>', methods=['GET'])
@jwt_required()
def get_review(review_id):
    # Querying a specific review and selecting it by the ID provided
    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)

    # Handling the Retrieved ID and retruning as JSON
    if review:
        return ReviewSchema().dump(review)
    else:
        # Retruning 404 if ID does not exist
        return {'error': 'Review not found'}, 404


@reviews_bp.route('/', methods=['POST'])
@jwt_required()
def new_review():
    try:
        # Sets current user variable to token
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

        # Creating a new review and committing to the database
        review = Review(
            title=review_info['title'],
            message=review_info['message'],
            product_id=product_id,
            user_id=current_user_id
        )

        db.session.add(review)
        db.session.commit()

        # Return the review as JSON
        return ReviewSchema().dump(review), 201

    # Else returns and Integrity Error 500
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Integrity error occurred while creating review'}), 500


@reviews_bp.route('/<int:review_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_review(review_id):
    # load the review information from request payload excluding some items
    review_info = ReviewSchema(exclude=['id', 'product_id'], partial=True).load(request.json)

    # Query the database for specific review by its ID
    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)

    # Handling retrieved data
    if review:
        # Check user authorisation before updating the review
        authorize(review.user_id)

        # Update review data if the review exists
        review.title = review_info.get('title', review.title)
        review.message = review_info.get('message', review.message)

        # Commit the changes to the database
        db.session.commit()

        # Return updated review data as JSON
        return ReviewSchema().dump(review)
    else:
        # Returns a 404 error if ID does not exist
        return {'error': 'Review not found'}, 404


@reviews_bp.route('/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    # Queries the database to retrieve the specific review by ID
    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)

    # Handles the retrieved data
    if review:
        # Authorize the user before deleting the review
        authorize(review.user_id)

        # Delete the selected review and commit changes to the database
        db.session.delete(review)
        db.session.commit()

        # Returns message if successful deletion of review
        return ({'message': 'Review deleted successfully'})
    else:
        # Returns error 404 if review does not exist
        return {'error': 'Review not found'}, 404
