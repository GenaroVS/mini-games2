import os
import logging
from flask import Flask, has_request_context, request
from flask.logging import default_handler
from werkzeug import exceptions
from . import minesweeper
from mongo import db

def create_app(test_config=None):

    class RequestFormatter(logging.Formatter):
        def format(self, record):
            if has_request_context():
                record.url = request.url
                record.remote_addr = request.remote_addr
            else:
                record.url = None
                record.remote_addr = None

            return super().format(record)

    formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )
    default_handler.setFormatter(formatter)

    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        if os.environ.get('FLASK_ENV') == 'production':
            app.config.from_object('config.Production', silent=True)
        else:
            app.config['MONGODB_SETTINGS'] = {
                'db': 'test',
                'host': 'mongodb://127.0.0.1:27017/test'
            }

    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(minesweeper.bp)

    @app.errorhandler(exceptions.BadRequest)
    def handle_bad_request(e):
        return 'Bad request!', 400

    @app.errorhandler(exceptions.InternalServerError)
    def handle_bad_request(e):
        return 'Internal server error!', 500

    db.init_app(app)
    return app