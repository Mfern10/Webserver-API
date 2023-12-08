from setup import db, ma 
from marshmallow import fields


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)

class CategorySchema(ma.Schema):
    name = fields.String(required=True)
    description = fields.String(required=True)

    class Meta:
        fields = ('id', 'name', 'description')
