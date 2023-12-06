from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://Roflgank3d:abc123@127.0.0.1:5432/web_server_api'

db = SQLAlchemy(app)



@app.route('/')
def index():
    return "success"

if __name__ == '__main__':
    app.run(debug=True)