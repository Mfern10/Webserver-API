from setup import db, ma
from marshmallow import fields
from marshmallow.validate import Length

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, default='Anonymous')
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    products = db.relationship('Product', back_populates='user')
    reviews = db.relationship('Review', back_populates='user')


class UserSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=Length(min=6, max=20, error='Password must be between 6 and 20 characters'))

    class Meta:
        fields = ('id', 'name', 'email', 'password', 'is_admin')