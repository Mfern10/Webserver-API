from setup import bcrypt, db
from flask import Blueprint, request, jsonify 
from models.user import UserSchema, User
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from auth import authorize
from datetime import timedelta
from marshmallow.validate import ValidationError

users_bp = Blueprint('users_bp', __name__, url_prefix='/users')

# Create new user


@users_bp.route('/register', methods=['POST'])
def register():
    try:
        # Load the user info from the request excluding items
        user_info = UserSchema(exclude=['id', 'is_admin']).load(request.json)


        # Check for email already in use
        existing_user = User.query.filter_by(email=user_info['email']).first()
        if existing_user:
            return jsonify({'error': 'Email address is already being used'}), 409
        
        if not all(key in user_info for key in ['name', 'email', 'password']):
            return jsonify({'error': 'Name, email and password are required'}), 404

        # Create a new User instance with a hashed password
        user = User(
            name=user_info['name'],
            email=user_info['email'],
            password=bcrypt.generate_password_hash(
                user_info['password']).decode('utf8')
        )

        # Add the new user to the database and commit the changes
        db.session.add(user)
        db.session.commit()

        # Return the new user information excluding the password for security
        return UserSchema(exclude=['password']).dump(user), 201
    except ValidationError as e:
        # Returns an error if the email address has already been used
        return jsonify({'error': 'Name, email and password is required'}), 400


# Get all users
@users_bp.route('/', methods=['GET'])
@jwt_required()
def all_users():
    # Use query to retrieve all users from the database
    # Using query.all() to get all users instead of scalar
    users = User.query.all()

    # Serialize the retrieved users using marshmallow schema
    # Ensure exclusion of password in seialized data
    users_schema = UserSchema(many=True, exclude=['password'])
    serialized_users = users_schema.dump(users)

    # Return the serialized users as a JSON response
    return jsonify(serialized_users), 200

# Get one user
@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def one_user(user_id):
    # Use query to retrieve all users from the database
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    if user:
        return UserSchema(exclude=['password']).dump(user), 200
    else:
        return {'error': 'User not found'}, 404



# Login user and create token


@users_bp.route('/login', methods=['POST'])
def login():
    # Deserialize incoming JSON request data using UserSchema
    user_info = UserSchema(
        exclude=['id', 'name', 'is_admin']).load(request.json)
    print(user_info)

    # Query the database to find a user with an email matching the one provided
    # Verify the password hash to authentice the user
    stmt = db.select(User).where(User.email == user_info['email'])
    user = db.session.scalar(stmt)

    if user and bcrypt.check_password_hash(user.password, user_info['password']):

        # Generate a JWT token for the authenticated user with and expiration time
        token = create_access_token(
            identity=user.id, expires_delta=timedelta(hours=8))

        # Return the JWT token and serialized user data excluding password for security
        return {'token': token, 'user': UserSchema(exclude=['password']).dump(user)}
    else:
        # Returns error message if provided login credentials are incorrect
        return {'error': 'Invalid email or password'}, 401

# Delete a user


@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    try:
        # Retrieve a specific user by their ID using a select query and scalar
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)

        # Handle the retrieved data
        if user:
            # Authorize the deletion by checking the users authorization
            authorize(user_id)

            # Delete the user and commit the changes to database
            db.session.delete(user)
            db.session.commit()

            # Return a message for successful deletion
            return ({'message': 'User deleted successfully'}), 200
        else:
            # Return error if the user ID is not found in the database
            return {'error': 'User not found'}, 404
    except AttributeError:
        # Return and error if the user is not authorized
        return {'error': 'You are not authorized to perform this action'}, 401
