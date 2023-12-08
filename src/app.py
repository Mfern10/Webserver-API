from setup import app
from blueprints.commands_bp import db_commands
from blueprints.users_bp import users_bp
from blueprints.categories_bp import categories_bp

app.register_blueprint(db_commands)
app.register_blueprint(users_bp)
app.register_blueprint(categories_bp)