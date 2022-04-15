from flask_app import db
from flask_scrypt import generate_password_hash, generate_random_salt, check_password_hash


class User(db.Model):
    __tablename__ = 'user'

    name = db.Column(db.String, primary_key=True)
    password_hash = db.Column(db.String)
    password_salt = db.Column(db.String)
    admin = db.Column(db.Boolean, default=False)
    count = db.relationship("Count", back_populates='user', uselist=False, cascade="delete, merge, save-update")

    def __init__(self, name: str, password: str, admin: bool = False) -> None:
        self.name = name
        self.set_password(password)
        self.admin = admin

    def is_active(self):
        return True

    def get_id(self):
        return self.name

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def set_password(self, password: str) -> None:
        salt = generate_random_salt()
        self.password_salt = salt
        self.password_hash = generate_password_hash(password, salt=salt)

    def check_password(self, password: str) -> bool:
        return check_password_hash(password, self.password_hash, self.password_salt)


