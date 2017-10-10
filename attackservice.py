from flask import Flask, request, send_file, jsonify
from flask_restplus import Resource, Api, reqparse, fields
from flask_cors import CORS

#import celery

import time
import os
import json
from werkzeug.exceptions import BadRequest


def create_app():
    app = Flask(__name__)

    CORS(app)
    api = Api(app)

    parser = reqparse.RequestParser()
    parser.add_argument('adrress', action='append', type=str, help='Target address')
    ns = api.namespace('TimeAttack', description='Timing attack operations')

    params = api.model('Params', {
        'xpos': fields.Integer(readOnly=True, description='X-position'),
        'ypos': fields.Integer(required=True, description='Y-position'),
        'samplerate': fields.Integer(required=True, description='Samplerate'),
        'duration': fields.Integer(required=True, description='Duration'),
        'frequency': fields.Integer(required=True, description='Frequency')
    })



    @ns.route('/attack/<string:address>')
    class Attacks(Resource):
        """ This endpoint initiates an attack """
        @ns.doc('post measurement parameters')
        @ns.expect(params)
        @ns.marshal_with(params)
        def post(self):
            # Start a celery task doing the task
            return


    @ns.route('/results')
    class Results(Resource):
        """ This endpoint returns results """
        @ns.doc('get a graph html')
        def get(self):
            #return the correct result
            return(html)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
