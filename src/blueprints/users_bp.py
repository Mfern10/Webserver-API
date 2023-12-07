from setup import bcrypt, db
from flask import Blueprint, request
from models.user import UserSchema, User
from sqlalchemy.exc import IntegrityError

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


