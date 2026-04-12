from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restful import Api

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'supersecretkey'

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # register all routes
    from routes import Signup, Login, Logout, CheckSession, NoteList, NoteDetail
    api = Api(app)
    api.add_resource(Signup, '/signup')
    api.add_resource(Login, '/login')
    api.add_resource(Logout, '/logout')
    api.add_resource(CheckSession, '/check_session')
    api.add_resource(NoteList, '/notes')
    api.add_resource(NoteDetail, '/notes/<int:id>')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(port=5555, debug=True)