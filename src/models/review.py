from setup import db, ma
from marshmallow import fields


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='reviews')

    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id'), nullable=False)
    product = db.relationship('Product', back_populates='reviews')


class ReviewSchema(ma.Schema):
    title = fields.String()
    message = fields.String()

    class Meta:
        fields = ('id', 'title', 'message', 'user_id', 'product_id')
