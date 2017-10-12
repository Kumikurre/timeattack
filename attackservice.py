from flask import Flask, request, send_file, jsonify
from flask_restplus import Resource, Api, reqparse, fields
from flask_cors import CORS

import time
import os
import json
from werkzeug.exceptions import BadRequest

from celery import Celery

def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery



def create_app():
    app = Flask(__name__)

    CORS(app)
    api = Api(app)

    parser = reqparse.RequestParser()
    parser.add_argument('resultid', action='append', type=str, help='ID of the result')
    ns = api.namespace('TimeAttack', description='Timing attack operations')

    params = api.model('Params', {
        'address': fields.Integer(readOnly=True, description='Attack target address'),
        'digits': fields.Integer(required=True, description='Number of digits in the password to be brute forced'),
        'resultname': fields.Integer(required=False, description='Result filename (optional)')
    })


    @ns.route('/attack')
    class Attacks(Resource):
        """ This endpoint initiates an attack """
        @ns.doc('post attack parameters and initiate attack')
        @ns.expect(params)
        @ns.marshal_with(params)
        def post(self):
            # Start a celery task doing the task
            return


    @ns.route('/results')
    class Results(Resource):
        """ This endpoint returns results """
        @ns.doc('fetch results')
        def get(self):
            #return the correct result
            return('results')

    @ns.route('/results/<string:resultid>')
    class Result(Resource):
        """ This endpoint returns a single result """
        @ns.doc('fetch a single result')
        def get(self):
            #return the correct result
            return('result')

    return app


if __name__ == '__main__':
    app = create_app()

    app.run(debug=True)
