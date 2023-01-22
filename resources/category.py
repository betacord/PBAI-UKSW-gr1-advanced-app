from flask import request
from flask_restful import Resource

from models.category import CategoryModel
from schemas.category import CategorySchema

category_schema = CategorySchema()


class Category(Resource):
    @classmethod
    def get(cls, slug: str) -> any:
        if category := CategoryModel.find_by_slug(slug):
            return category_schema.dump(category), 200

        return {'message': 'Category not found'}, 404

    @classmethod
    def post(cls, slug: str) -> any:
        if CategoryModel.find_by_name(slug):
            return {'message': 'Category with this name already exists'}, 400

        category_json = request.get_json()

        category = CategoryModel(
            name=category_json['name'],
            description=category_json['description']
        )

        try:
            category.save()
        except Exception as e:
            return {'message': e}, 500

        return category_schema.dump(category), 201

    @classmethod
    def delete(cls, slug: str) -> any:
        if category := CategoryModel.find_by_slug(slug):
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
            category.description = category_json['description']

            try:
                category.save()
            except Exception as e:
                return {'message': e}, 500

            return category_schema.dump(category), 202

        return {'message': 'Category not found'}, 404
