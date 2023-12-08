from setup import db, bcrypt
from flask import Blueprint
from models.user import User

db_commands = Blueprint('db', __name__)

# adds a terminal function to run to create the table
@db_commands.cli.command('create')
def db_create():
    db.drop_all() # drops the tables when run so no duplicates
    db.create_all()
    print('Created tables')

# creates a terminal function to run that places data into the table
@db_commands.cli.command('seed')
def db_seed():
    users = [
        User(
            name = 'Mitchell',
            email = 'admin@catalogue.com',
            password=bcrypt.generate_password_hash('password').decode('utf8'),
            is_admin=True
        ),
        User(
            name = 'Bob Smith',
            email = 'bob@catalogue.com',
            password=bcrypt.generate_password_hash('iambob').decode('utf8'),
            is_admin=False
        ),
        User(
            name = 'Lee Smith',
            email = 'lee@catalogue.com',
            password=bcrypt.generate_password_hash('iamlee').decode('utf8'),
            is_admin=False
        )
    ]
    print("Tables seeded")

    db.session.add_all(users)
    db.session.commit()