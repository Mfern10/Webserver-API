from setup import db, ma 
from marshmallow import fields


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='reviews')

class CategorySchema(ma.Schema):
    title = fields.String(required=True)
    message = fields.String(required=True)

    class Meta:
        fields = ('id', 'title', 'message')