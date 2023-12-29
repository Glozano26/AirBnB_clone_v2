#!/usr/bin/python3
"""
Contains the app_views
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage

# app_views = Flask(__name__)


@app_views.route('/status')
def status():
    """"functions that return JSON"""
    data = {'status': 'OK'}
    return jsonify(data)


@app_views.route('/api/v1/stats')
def counts():
    """Create an endpoint that retrieves the number of each objects by type"""
    dat_endp = storage.count()
    return jsonify(dat_endp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)