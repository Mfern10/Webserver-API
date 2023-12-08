from setup import db
from flask import Blueprint


categories_bp = Blueprint('categories_bp', __name__, url_prefix='/categories')