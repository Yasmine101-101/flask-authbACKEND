from app import db
from app import db, bcrypt


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    # username must be unique so it can be used as an identifier
    username = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String, nullable=False)

    # notes relationship - user has many notes
    notes = db.relationship('Note', back_populates='user', cascade='all, delete-orphan')

    # hash the password before saving it
    @property
    def password(self):
        raise AttributeError("password is not readable")

    @password.setter
    def password(self, plaintext_password):
        self._password_hash = bcrypt.generate_password_hash(plaintext_password).decode('utf-8')

    # check if the password is correct
    def check_password(self, plaintext_password):
        return bcrypt.check_password_hash(self._password_hash, plaintext_password)
# define models here