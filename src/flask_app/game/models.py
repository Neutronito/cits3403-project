from flask_app import db


class Count(db.Model):
    __tablename__ = 'count'

    username = db.Column(db.String, db.ForeignKey('user.name'), primary_key=True)
    count = db.Column(db.Integer)
    user = db.relationship("User", back_populates='count', cascade="delete, merge, save-update")

    def __init__(self, username: str, count: int = 0) -> None:
        self.username = username
        self.count = count