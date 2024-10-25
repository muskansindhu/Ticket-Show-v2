from flask import Flask
from application.config import Config, KEY
from application.database import db
from flask_restful import Api
from flask_cors import CORS
from application import workers




def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*":{'origins':"*"}})
    app.config.from_object(Config)
    app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
    app.static_folder = 'static'
    with open(KEY) as key_file:
        app.secret_key = bytes(key_file.readline(), 'utf-8')
    app.app_context().push()

    db.init_app(app)
    with app.app_context():
        from application.models import Admin, User, Theater, Show, Booking
        db.create_all()

    # Initialize Celery
    celery = workers.celery
    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
    )
    celery.Task = workers.ContextTask
    app.app_context().push()


    return app, celery


app, celery=create_app()

from application.api import AdminAPI, UserAPI, TheaterAPI, ShowAPI, BookingAPI
api = Api(app)

api.add_resource(AdminAPI,"/api/admin", "/api/admin/<username>")
api.add_resource(UserAPI,"/api/user", "/api/user/<username>")
api.add_resource(TheaterAPI,"/api/theater", "/api/theater/<theater_id>")
api.add_resource(ShowAPI, "/api/theater/<int:theater_id>/show", "/api/theater/<int:theater_id>/show/<int:show_id>","/api/theater/show/<int:show_id>")
api.add_resource(BookingAPI, "/api/booking/<int:user_id>/<int:show_id>", "/api/booking/<int:user_id>")

from application.controller import *

if __name__=='__main__':
    app.run(host='0.0.0.0', port=1234, debug=True)