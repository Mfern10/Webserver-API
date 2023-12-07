from setup import bcrypt, db
from flask import Blueprint, request, jsonify
from models.user import UserSchema, User
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token
from datetime import timedelta 

users_bp = Blueprint('users_bp', __name__, url_prefix='/users')


@users_bp.route('/register', methods=['POST'])
def register():
    try:
        user_info = UserSchema(exclude=['id', 'is_admin']).load(request.json)
        user = User(
            name=user_info['name'],
            email=user_info['email'],
            password=bcrypt.generate_password_hash(user_info['password']).decode('utf8')
        )
        # Add and commit the new user information
        db.session.add(user)
        db.session.commit()
        # Return the new user information
        return UserSchema(exclude=['password']).dump(user), 201
    except IntegrityError:
        return {'error': 'Email address is already being used'}, 409
    
# gets all users ** make sure it is authroized for admins only **
@users_bp.route('/', methods=['GET'])
def all_users():
    # use query to retrieve all users from the database, Using query.all() instead of scalar
    # as scalar is better for a single user but here I want to retrieve all users from the database.
    users = User.query.all()
    
    # Serialize the users using Marshamllow schema making sure to exclude passwords
    users_schema = UserSchema(many=True, exclude=['password'])
    serialized_users = users_schema.dump(users)

    # Return the serialized users as a JSON response
    return jsonify(serialized_users), 200

@users_bp.route('/login', methods = ['POST'])
def login():
    # Parse incoming POST body through user schema
    user_info = UserSchema(exclude=['id', 'name', 'is_admin']).load(request.json)
    print(user_info)
    
    # Select the user with email that matches the one in the POST body using select query and scalar
    # Cross check the password hash
    stmt = db.select(User).where(User.email == user_info['email'])
    user = db.session.scalar(stmt)
    if user and bcrypt.check_password_hash(user.password, user_info['password']):
        
        # Create a JWT token for the user
        token = create_access_token(identity=user.id, expires_delta=timedelta(hours=8))
        
        # Return the JWT token or error if login details dont match
        return {'token': token, 'user': UserSchema(exclude=['password']).dump(user)}
    else: 
        return {'error': 'Invalid email or password'}, 401





