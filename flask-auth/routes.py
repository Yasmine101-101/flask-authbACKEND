from flask import request, session, jsonify
from flask_restful import Resource
from models import User
from app import db


# POST /signup - create a new user
class Signup(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # make sure username and password are provided
        if not username or not password:
            return {'error': 'Username and password are required'}, 400

        # check if username already exists
        if User.query.filter_by(username=username).first():
            return {'error': 'Username already taken'}, 409

        # create the new user
        user = User(username=username)
        user.password = password
        db.session.add(user)
        db.session.commit()

        # log them in straight away
        session['user_id'] = user.id
        return {'id': user.id, 'username': user.username}, 201


# POST /login - log in a user
class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # find the user by username
        user = User.query.filter_by(username=username).first()

        # check if user exists and password is correct
        if not user or not user.check_password(password):
            return {'error': 'Invalid username or password'}, 401

        # save user id in session
        session['user_id'] = user.id
        return {'id': user.id, 'username': user.username}, 200


# DELETE /logout - log out a user
class Logout(Resource):
    def delete(self):
        # check if user is logged in
        if not session.get('user_id'):
            return {'error': 'Not logged in'}, 401

        # clear the session
        session.pop('user_id', None)
        return {}, 204


# GET /check_session - check if user is logged in
class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')

        # if no user in session return 401
        if not user_id:
            return {'error': 'Unauthorized'}, 401

        user = User.query.get(user_id)
        return {'id': user.id, 'username': user.username}, 200