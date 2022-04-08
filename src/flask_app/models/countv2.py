from .. import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    password_hash = db.Column(db.String)
    password_salt = db.Column(db.String)
    count = db.relationship("Count", back_populates='user', uselist=False)


class Count(db.Model):
    __tablename__ = 'count'
    
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    count = db.Column(db.Integer)
    user = db.relationship("User", back_populates='count')

