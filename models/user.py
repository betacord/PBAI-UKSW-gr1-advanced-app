from __future__ import annotations

from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255))

    categories = db.relationship('CategoryModel', backref='user', lazy='dynamic')
    courses = db.relationship('CourseModel', backref='user', lazy='dynamic')

    @classmethod
    def find_by_id(cls, id_: int) -> UserModel:
        return cls.query.filter_by(id=id_).first()

    @classmethod
    def find_by_username(cls, username: str) -> UserModel:
        return cls.query.filter_by(username=username).first()

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()
