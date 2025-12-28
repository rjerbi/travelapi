# app.py
from flask import Flask
from config import Config
from extensions import mongo, ma, jwt # Changed db to mongo
from routes import api_bp
# Removed from flask_migrate import Migrate
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # Initialize extensions
    mongo.init_app(app) # Changed db.init_app to mongo.init_app
    ma.init_app(app)
    jwt.init_app(app)
    # Register blueprint
    app.register_blueprint(api_bp, url_prefix='/api')
    # Removed db.create_all() as MongoDB is schemaless
    # Removed Flask-Migrate initialization
    return app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
