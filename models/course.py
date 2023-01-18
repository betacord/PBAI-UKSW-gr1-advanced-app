from slugify import slugify

from db import db


class CourseModel(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String, unique=True, nullable=False)
    slug = db.Column(db.String(150), unique=True, nullable=False)
    video_url = db.Column(db.String(150), unique=True, nullable=False)

    @classmethod
    def find_by_slug(cls, slug: str) -> 'CourseModel':
        return cls.query.filter_by(slug=slug).first()

    @classmethod
    def find_by_name(cls, name: str) -> 'CourseModel':
        return cls.query.filter_by(name=name).first()

    def save(self) -> None:
        self.slug = slugify(self.name)

        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()
