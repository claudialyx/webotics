from app import app
from flask import render_template
from flask_assets import Environment, Bundle

assets = Environment(app)

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route("/")
def home():
    return "THIS IS HOME"
