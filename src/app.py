from setup import app
from blueprints.commands_bp import db_commands
from blueprints.users_bp import users_bp
from blueprints.categories_bp import categories_bp
from blueprints.products_bp import products_bp
from blueprints.reviews_bp import reviews_bp

app.register_blueprint(db_commands)
app.register_blueprint(users_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(products_bp)
app.register_blueprint(reviews_bp)
