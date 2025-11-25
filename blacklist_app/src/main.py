import os
import newrelic.agent
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from .db.database import init_db, create_tables
from .routes.blacklist_router import blacklist_bp

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEW_RELIC_CONFIG = os.path.join(BASE_DIR, "newrelic.ini")

newrelic.agent.initialize(NEW_RELIC_CONFIG)

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Wrap app with New Relic WSGI wrapper
app = newrelic.agent.WSGIApplicationWrapper(app)

# Configure CORS
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Initialize database
init_db(app)

# Register blueprints
app.register_blueprint(blacklist_bp)

# Create database tables on startup
with app.app_context():
    create_tables(app)

# Global error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Not Found",
        "message": "The requested resource was not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal Server Error",
        "message": "An unexpected error occurred"
    }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)