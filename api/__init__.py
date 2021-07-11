import os
import logging
from flask import Flask, has_request_context, request
from flask_cors import CORS
from flask.logging import default_handler
from werkzeug import exceptions
import api.minesweeper as ms

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
            app.config['MONGODB_SETTINGS'] = {
                'db': 'arcade',
                'host': os.environ.get('MONGODB_URI')
            }
        else:
            app.config['MONGODB_SETTINGS'] = {
                'db': 'arcade',
                'host': 'mongodb://127.0.0.1:27017/arcade'
            }
    else:
        app.config.from_mapping(test_config)

    CORS(app, origins=['http://localhost:3000', 'http://games.gvsalinas.com, http://localhost:80'])

    from api.mongo import db
    db.init_app(app)

    app.register_blueprint(ms.bp)

    @app.route('/', methods=['GET','POST'])
    def default():
        return '<h1 style="text-align:center">mini-games.gvsalinas.com API</h1>'

    @app.errorhandler(exceptions.BadRequest)
    def handle_bad_request(e):
        return 'Bad request!', 400

    @app.errorhandler(exceptions.InternalServerError)
    def handle_bad_request(e):
        return 'Internal server error!', 500

    return app