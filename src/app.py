from setup import app
from flask import jsonify
from blueprints.commands_bp import db_commands
from blueprints.users_bp import users_bp
from blueprints.categories_bp import categories_bp
from blueprints.products_bp import products_bp
from blueprints.reviews_bp import reviews_bp
from marshmallow import ValidationError


# Blueprint Registry
app.register_blueprint(db_commands)
app.register_blueprint(users_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(products_bp)
app.register_blueprint(reviews_bp)


# Generic error handling for application
@app.errorhandler(ValidationError)
def validation_error_handler(error):
    return jsonify.error({'error': error.messages}), 400

@app.errorhandler(Exception)
def unexpected_error_handler(error):
    app.logger.error(f"An unexpected error occurred: {error}")
    return jsonify({'error': 'An unexpected error occurred'}), 500


