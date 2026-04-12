from flask import request, session, jsonify
from flask_restful import Resource
from functools import wraps
from models import User, Note
from app import db


# decorator to protect routes - reusable on any route
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Unauthorized - please log in'}, 401
        return f(*args, **kwargs)
    return decorated


# helper function to get current logged in user
def get_current_user():
    user_id = session.get('user_id')
    if not user_id:
        return None
    return User.query.get(user_id)


# POST /signup - create a new user
class Signup(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {'error': 'Username and password are required'}, 400

        if User.query.filter_by(username=username).first():
            return {'error': 'Username already taken'}, 409

        user = User(username=username)
        user.password = password
        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id
        return {'id': user.id, 'username': user.username}, 201


# POST /login - log in a user
class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            return {'error': 'Invalid username or password'}, 401

        session['user_id'] = user.id
        return {'id': user.id, 'username': user.username}, 200


# DELETE /logout - log out a user
class Logout(Resource):
    @login_required
    def delete(self):
        session.pop('user_id', None)
        return {}, 204


# GET /check_session - check if user is logged in
class CheckSession(Resource):
    def get(self):
        user = get_current_user()
        if not user:
            return {'error': 'Unauthorized'}, 401
        return {'id': user.id, 'username': user.username}, 200


# GET /notes - get all notes for logged in user with pagination
# POST /notes - create a new note
class NoteList(Resource):
    @login_required
    def get(self):
        user = get_current_user()

        # pagination - default page 1, 10 notes per page
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        # only get notes that belong to this user
        notes = Note.query.filter_by(user_id=user.id).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return {
            'notes': [
                {
                    'id': note.id,
                    'title': note.title,
                    'content': note.content,
                    'created_at': str(note.created_at)
                }
                for note in notes.items
            ],
            'total': notes.total,
            'page': notes.page,
            'pages': notes.pages
        }, 200

    @login_required
    def post(self):
        user = get_current_user()
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')

        if not title or not content:
            return {'error': 'Title and content are required'}, 400

        note = Note(
            title=title,
            content=content,
            user_id=user.id
        )
        db.session.add(note)
        db.session.commit()

        return {
            'id': note.id,
            'title': note.title,
            'content': note.content,
            'created_at': str(note.created_at)
        }, 201


# PATCH /notes/<id> - update a note
# DELETE /notes/<id> - delete a note
class NoteDetail(Resource):
    @login_required
    def patch(self, id):
        user = get_current_user()
        note = Note.query.get(id)

        if not note:
            return {'error': 'Note not found'}, 404

        # users can only update their own notes
        if note.user_id != user.id:
            return {'error': 'Unauthorized'}, 401

        data = request.get_json()
        if 'title' in data:
            note.title = data['title']
        if 'content' in data:
            note.content = data['content']

        db.session.commit()

        return {
            'id': note.id,
            'title': note.title,
            'content': note.content,
            'created_at': str(note.created_at)
        }, 200

    @login_required
    def delete(self, id):
        user = get_current_user()
        note = Note.query.get(id)

        if not note:
            return {'error': 'Note not found'}, 404

        # users can only delete their own notes
        if note.user_id != user.id:
            return {'error': 'Unauthorized'}, 401

        db.session.delete(note)
        db.session.commit()
        return {}, 204