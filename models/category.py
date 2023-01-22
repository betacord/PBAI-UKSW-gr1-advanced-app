from __future__ import annotations

from slugify import slugify

from db import db


class CategoryModel(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String, unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=True)

    courses = db.relationship('CourseModel', backref='category', lazy='dynamic')

    @classmethod
    def find_all(cls) -> list[CategoryModel]:
        return cls.query.all()

    @classmethod
    def find_by_id(cls, id_: int) -> CategoryModel:
        return cls.query.filter_by(id=id_).first()

    @classmethod
    def find_by_slug(cls, slug: str) -> CategoryModel:
        return cls.query.filter_by(slug=slug).first()

    @classmethod
    def find_by_name(cls, name: str) -> CategoryModel:
        return cls.query.filter_by(name=name).first()

    def save(self) -> None:
        self.slug = slugify(self.name)

        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()
