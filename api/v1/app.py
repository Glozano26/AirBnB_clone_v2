#!/usr/bin/python3
"""Contains entrypoint"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views


app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def clean_up_all(exc):
    """Cleaning function to be executed at
    end application context"""
    storage.close()

@app.errorhandler(404)
def error(e):
    """Return messagge Not found"""
    dict_response = {"error": "Not found"}
    dict_response.status_code = 404
    return jsonify(dict_response)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', threaded=True)
