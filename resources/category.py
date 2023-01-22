from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from models.category import CategoryModel
from schemas.category import CategorySchema

category_schema = CategorySchema()
category_list_schema = CategorySchema(many=True)


class Category(Resource):
    @classmethod
    def get(cls, slug: str) -> any:
        if category := CategoryModel.find_by_slug(slug):
            return category_schema.dump(category), 200

        return {'message': 'Category not found'}, 404

    @classmethod
    @jwt_required()
    def post(cls, slug: str) -> any:
        if CategoryModel.find_by_name(slug):
            return {'message': 'Category with this name already exists'}, 400

        category_json = request.get_json()

        category = CategoryModel(
            name=category_json['name'],
            description=category_json['description'],
            user_id=get_jwt_identity()
        )

        try:
            category.save()
        except Exception as e:
            return {'message': e}, 500

        return category_schema.dump(category), 201

    @classmethod
    @jwt_required()
    def delete(cls, slug: str) -> any:
        if category := CategoryModel.find_by_slug(slug):
            if category.user_id != get_jwt_identity():
                return {'message': 'Access denied'}, 403

            try:
                category.delete()
            except Exception as e:
                return {'message': e}, 500

            return {'message': 'Category deleted successfully'}, 202

        return {'message': 'Category not found'}, 404

    @classmethod
    def put(cls, slug: str) -> any:
        category_json = request.get_json()

        if category := CategoryModel.find_by_slug(slug):
            if category.user_id != get_jwt_identity():
                return {'message': 'Access denied'}, 403

            category.description = category_json['description']

            try:
                category.save()
            except Exception as e:
                return {'message': e}, 500

            return category_schema.dump(category), 202

        return {'message': 'Category not found'}, 404


class CategoryList(Resource):
    @classmethod
    def get(cls) -> any:
        return {'categories': category_list_schema.dump(CategoryModel.find_all())}, 200
