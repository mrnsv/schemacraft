"""Flask application entry point for JSON Schema generation"""

from flask import Flask
from routes import bp

app = Flask(__name__)

app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=False)  # Disable debug mode in production
