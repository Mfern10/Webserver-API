from setup import db, ma 
from marshmallow import fields


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    color = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.Date, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='products')

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Category', back_populates='products')


class ProductSchema(ma.Schema):
    name = fields.String(required=True)
    description = fields.String(required=True)

    class Meta:
        fields = ('id', 'name', 'description', 'price', 'color', 'date_created')