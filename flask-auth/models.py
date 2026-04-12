from app import db, bcrypt


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    # username must be unique so it can be used as an identifier
    username = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String, nullable=False)

    # user has many notes
    notes = db.relationship('Note', back_populates='user', cascade='all, delete-orphan')

    @property
    def password(self):
        raise AttributeError("password is not readable")

    @password.setter
    def password(self, plaintext_password):
        self._password_hash = bcrypt.generate_password_hash(plaintext_password).decode('utf-8')

    def check_password(self, plaintext_password):
        return bcrypt.check_password_hash(self._password_hash, plaintext_password)


class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    # title and content are the 2 custom fields
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    # created_at so we can sort notes by date
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # foreign key linking note to a user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # note belongs to a user
    user = db.relationship('User', back_populates='notes')