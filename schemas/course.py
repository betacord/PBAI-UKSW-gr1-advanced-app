from ma import ma
from models.course import CourseModel


class CourseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CourseModel
        dump_only = ('slug', 'id', 'user_id')
        load_instance = True
        include_fk = True
