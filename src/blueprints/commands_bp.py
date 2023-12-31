from setup import db, bcrypt
from flask import Blueprint
from models.user import User
from models.category import Category
from models.product import Product
from datetime import datetime
from models.review import Review

db_commands = Blueprint('db', __name__)

# adds a terminal function to run to create the table


@db_commands.cli.command('create')
def db_create():
    db.drop_all()  # drops the tables when run so no duplicates
    db.create_all()
    print('Created tables')

# creates a terminal function to run that places data into the table


@db_commands.cli.command('seed')
def db_seed():
    users = [
        User(
            name='Mitchell',
            email='admin@catalogue.com',
            password=bcrypt.generate_password_hash('password').decode('utf8'),
            is_admin=True
        ),
        User(
            name='Bob Smith',
            email='bob@catalogue.com',
            password=bcrypt.generate_password_hash('iambob').decode('utf8'),
            is_admin=False
        ),
        User(
            name='Lee Smith',
            email='lee@catalogue.com',
            password=bcrypt.generate_password_hash('iamlee').decode('utf8'),
            is_admin=False
        ),

    ]
    categories = [
        Category(
            name='Tops',
            description='A collection of upper body clothing including, T-shirts, Hoodies, sweaters, singlets etc'
        ),
        Category(
            name='Bottoms',
            description='A collection of bottoms including, Jeans, Joggers, Pants, Chinos etc'
        ),
        Category(
            name='Hats',
            description='A collection of headwear including beanies, baseball caps, trucker caps, bucket hats etc'
        )
    ]

    products = [
        Product(
            name='Nest Logo Tee',
            description='Premium organic cotton, tall fit t-shirt with nest logo embroided',
            price='59.99',
            color='Black',
            date_created=datetime.today(),
            user_id=1,
            category_id=1
        ),
        Product(
            name='Nest Demin Jeans',
            description='Premium Skinny leg, stretch fabric jeans with embroided nest logo.',
            price='69.99',
            color='Navy',
            date_created=datetime.today(),
            user_id=1,
            category_id=2
        ),
        Product(
            name='Nest Ribbed Beanie',
            description='Premium organic cotton, ribbed fit reversible beanie, great for winter',
            price='29.99',
            color='Black',
            date_created=datetime.today(),
            user_id=1,
            category_id=3
        )
    ]
    reviews = [
        Review(
            title='4 stars',
            message='A Great T-Shirt, very comfortable',
            user_id=1,
            product_id=1
        ),
        Review(
            title='Great fit',
            message='These skinny jeans feel great just the right stretching and very tough',
            user_id=2,
            product_id=2
        ),
        Review(
            title='SO WARM!',
            message='This beanie is super warm and great for winter weather',
            user_id=3,
            product_id=3
        )
    ]
    print("Tables seeded")

    db.session.add_all(users)
    db.session.add_all(categories)
    db.session.add_all(products)
    db.session.add_all(reviews)
    db.session.commit()
