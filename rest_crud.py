import re
from flask_restful import Resource, abort, marshal_with, fields
from sqlalchemy.exc import IntegrityError


def abort_if_not_exist(entry):
    if not entry:
        abort(404, message="Not found!")


def snake_case_name(model):
    name = model.__name__
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def add_collection(api, db, model):
    endpoint_item = snake_case_name(model) + '_item'
    endpoint_list = snake_case_name(model) + '_collection'
    collection_name = snake_case_name(model) + 's'
    parser = model.req_parser()

    class ManagedResource(Resource):

        @marshal_with(model.json())
        def get(self, model_id):
            entry = model.query.get(model_id)
            abort_if_not_exist(entry)
            return entry

        def delete(self, model_id):
            entry = model.query.get(model_id)
            abort_if_not_exist(entry)
            db.session.delete(entry)
            return '', 204

    class ManagedResourceList(Resource):

        @marshal_with(model.json())
        def get(self):
            all_models = model.query.all()
            return all_models

        def post(self):
            args = parser.parse_args()
            entry = model(**args)
            db.session.add(entry)
            # try:
            db.session.commit()
            return '', 302, {'Location': '/{}/{}'.format(collection_name, entry.id)}
            # except IntegrityError:
            #     # TODO: Respond with something more meaningful
            #     return 'Bad arguments', 400

    api.add_resource(ManagedResourceList, '/{}'.format(collection_name), endpoint=endpoint_list)
    api.add_resource(ManagedResource, '/{}/<model_id>'.format(collection_name), endpoint=endpoint_item)
