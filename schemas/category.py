from ma import ma
from models.category import CategoryModel
from schemas.course import CourseSchema


class CategorySchema(ma.SQLAlchemyAutoSchema):
    courses = ma.Nested(CourseSchema, many=True)

    class Meta:
        model = CategoryModel
        dump_only = ('slug', 'id')
        load_instance = True
