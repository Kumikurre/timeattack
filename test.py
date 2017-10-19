from flask import Flask, request, send_file, jsonify
from flask_restplus import Resource, Api, reqparse, fields
from flask_cors import CORS

from werkzeug.exceptions import BadRequest

import time
import os
import json
import requests
import time

username = test
password = a2nF

def login_comparison(username_try, password_try):
    if username_try == username:
        if password_try == password:
            return(True)
    else:
        return False

def create_app():
    app = Flask(__name__)
    CORS(app)
    api = Api(app)

    parser = reqparse.RequestParser()
    parser.add_argument('resultid', action='append', type=str, help='ID of the result')
    ns = api.namespace('Login', description='Very legit login service')

    params = api.model('Params', {
        'password': fields.String(required=True, description='Password'),
        'username': fields.String(required=True, description='Username')
    })


    @ns.route('/login')
    class Attacks(Resource):
        """ This endpoint initiates an attack """
        @ns.doc('post attack parameters and initiate attack')
        @ns.expect(params)
        @ns.marshal_with(params)
        def post(self):
            data = api.payload
            print(data)
            username_try = data['password']
            password_try = data['username']
            login_result = login_comparison(username_try, password_try)
            return(resultname)

    return app


if __name__ == '__main__':
    app = create_app()

    app.run(debug=True)
