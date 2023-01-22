from flask_restful import Resource
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from models.course import CourseModel
from schemas.course import CourseSchema

course_schema = CourseSchema()
course_list_schema = CourseSchema(many=True)


class Course(Resource):
    @classmethod
    def get(cls, slug: str) -> any:
        if course := CourseModel.find_by_slug(slug):
            return course_schema.dump(course), 200

        return {'message': 'Course not found'}, 404

    @classmethod
    @jwt_required()
    def post(cls, slug: str) -> any:
        if CourseModel.find_by_name(slug):
            return {'message': 'Course with this slug already exists'}, 400

        course_json = request.get_json()
        course_json['name'] = slug

        course = course_schema.load(course_json)

        course.user_id = get_jwt_identity()

        try:
            course.save()
        except Exception as e:
            return {'message': e}, 500

        return course_schema.dump(course), 201

    @classmethod
    @jwt_required()
    def delete(cls, slug: str) -> any:
        if course := CourseModel.find_by_slug(slug):
            if course.user_id != get_jwt_identity():
                return {'message': 'Access denied'}, 403

            try:
                course.delete()
            except Exception as e:
                return {'message': e}, 500

            return {'message': 'Course removed successfully'}, 202

        return {'message': 'Course not found'}, 404

    @classmethod
    @jwt_required()
    def put(cls, slug: str) -> any:
        course_json = request.get_json()

        if course := CourseModel.find_by_slug(slug):
            if course.user_id != get_jwt_identity():
                return {'message': 'Access denied'}, 403

            course.description = course_json['description']
            course.video_url = course_json['video_url']

            try:
                course.save()
            except Exception as e:
                return {'message': e}, 500

            return course_schema.dump(course), 202

        return {'message': 'Course not found'}, 404


class CourseList(Resource):
    @classmethod
    def get(cls) -> any:
        return {'courses': course_list_schema.dump(CourseModel.find_all())}, 200
