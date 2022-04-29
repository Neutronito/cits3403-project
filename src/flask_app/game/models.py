from __future__ import annotations

from datetime import date as date_object, datetime
from flask_app import db


class Count(db.Model):
    __tablename__ = 'count'

    date = db.Column(db.Date, primary_key=True)
    username = db.Column(db.String, db.ForeignKey('user.name'), primary_key=True)
    count = db.Column(db.Integer)
    user = db.relationship("User", back_populates='count', cascade="delete, merge, save-update")

    def __init__(self, username: str, count: int = 0, date: date_object | None = None) -> None:
        self.username = username
        self.count = count
        if date is None:
            self.date = datetime.utcnow().today()
        else:
            self.date = date

    def get_total_count(self) -> int:
        return db.session.query(db.func.sum(Count.count)).filter_by(username=self.username).first()[0]
