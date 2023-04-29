#!/usr/bin/python3
"""
The app file that runs
the app handles other functions
"""
from api.v1.views import app_views
from flask import Flask
from flask_cors import CORS
from models import storage
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontext(exception):
    """close storage"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """404 error"""
    return {"error": "Not found"}, 404


if __name__ == "__main__":
    """run app"""
    if getenv("HBNB_API_HOST"):
        host = getenv("HBNB_API_HOST")
    else:
        host = "0.0.0.0"
    if getenv("HBNB_API_PORT"):
        port = int(getenv("HBNB_API_PORT"))
    else:
        port = 5000
    app.run(host=host, port=port, threaded=True)
