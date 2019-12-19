import json

from django.http import HttpResponse
from django.views.generic import View

from restapi.mixins import HttpResponseMixin
from updates.forms import UpdateForm
from updates.models import Update

from .mixins import CSRFExemptMixin
from .utils import is_json


class UpdateModelDetailAPIView(HttpResponseMixin, CSRFExemptMixin, View):
    is_json = True

    def get_object(self, pk=None):
        qs = Update.objects.filter(pk=pk)
        if qs.count() == 1:
            return qs.first()
        return None

    def get(self, request, pk, *args, **kwargs):
        obj = self.get_object(pk=pk)
        if obj is None:
            error_data = json.dumps({'message': 'Update not found'})
            return self.render_to_response(error_data, status=404)
        json_data = obj.serialize()
        return self.render_to_response(json_data)

    def post(self, request, *args, **kwargs):
        json_data = json.dumps({'message': 'Not allowed, please use the api/updates/ endpoint'})
        return self.render_to_response(json_data, status=403)

    def put(self, request, pk, *args, **kwargs):
        valid_json = is_json(request.body)
        if not valid_json:
            error_data = json.dumps({'message': 'Invalid data sent, please send using JSON'})
            return self.render_to_response(error_data, status=400)

        obj = self.get_object(pk=pk)
        if obj is None:
            error_data = json.dumps({'message': 'Update not found'})
            return self.render_to_response(error_data, status=404)

        # new_data = {}
        data = json.loads(obj.serialize())
        passed_data = json.loads(request.body)
        for key, value in passed_data.items():
            data[key] = value

        form = UpdateForm(data, instance=obj)
        if form.is_valid():
            obj = form.save(commit=True)
            obj_data = json.dumps(data)
            return self.render_to_response(obj_data, status=201)
        if form.errors:
            data = json.dumps(form.errors)
            return self.render_to_response(data, status=400)

        json_data = json.dumps({'message': 'something'})
        return self.render_to_response(json_data)

    def delete(self, request, pk, *args, **kwargs):
        obj = self.get_object(pk=pk)
        if obj is None:
            error_data = json.dumps({'message': 'Update not found'})
            return self.render_to_response(error_data, status=404)
        deleted, item_deleted = obj.delete()
        if deleted == 1:
            json_data = json.dumps({'message': 'Successfully deleted.'})
            return self.render_to_response(json_data, status=200)
        error_data = json.dumps({'message': 'Couldn\'t delete item, please try again later.'})
        return self.render_to_response(error_data, status=400)


class UpdateModelListAPIView(HttpResponseMixin, CSRFExemptMixin, View):
    is_json = True
    queryset = None

    def get_queryset(self):
        qs = Update.objects.all()
        self.queryset = qs
        return qs

    def get_object(self, pk=None):
        if pk is None:
            return None
        qs = self.get_queryset().filter(pk=pk)
        if qs.count() == 1:
            return qs.first()
        return None

    def get(self, request, *args, **kwargs):
        data = json.loads(request.body)
        passed_pk = data.get('pk', None)
        if passed_pk is not None:
            obj = self.get_object(pk=passed_pk)
            if obj is None:
                error_data = json.dumps({'message': 'Object not found'})
                return self.render_to_response(error_data, status=404)
            json_data = obj.serialize()
            return self.render_to_response(json_data)
        else:
            qs = self.get_queryset()
            json_data = qs.serialize()
            return self.render_to_response(json_data)

    def post(self, request, *args, **kwargs):
        valid_json = is_json(request.body)
        if not valid_json:
            error_data = json.dumps({'message': 'Invalid data sent, please send using JSON'})
            return self.render_to_response(error_data, status=400)
        data = json.loads(request.body)
        form = UpdateForm(data)
        if form.is_valid():
            obj = form.save(commit=True)
            obj_data = obj.serialize()
            return self.render_to_response(obj_data, status=201)
        if form.errors:
            data = json.dumps(form.errors)
            return self.render_to_response(data, status=400)
        data = {'message': 'Not Allowed'}
        return self.render_to_response(data, status=400)

    def put(self, request, *args, **kwargs):
        valid_json = is_json(request.body)
        if not valid_json:
            error_data = json.dumps({'message': 'Invalid data sent, please send using JSON'})
            return self.render_to_response(error_data, status=400)

        passed_data = json.loads(request.body)
        passed_pk = passed_data.get('pk', None)
        if not passed_pk:
            error_data = json.dumps({'pk': 'This is a required field to update an item.'})
            return self.render_to_response(error_data, status=400)

        obj = self.get_object(pk=passed_pk)
        if obj is None:
            error_data = json.dumps({'message': 'Object not found'})
            return self.render_to_response(error_data, status=404)

        # new_data = {}
        data = json.loads(obj.serialize())
        for key, value in passed_data.items():
            data[key] = value

        form = UpdateForm(data, instance=obj)
        if form.is_valid():
            obj = form.save(commit=True)
            obj_data = json.dumps(data)
            return self.render_to_response(obj_data, status=201)
        if form.errors:
            data = json.dumps(form.errors)
            return self.render_to_response(data, status=400)

        json_data = json.dumps({'message': 'something'})
        return self.render_to_response(json_data)

    def delete(self, request, *args, **kwargs):
        valid_json = is_json(request.body)
        if not valid_json:
            error_data = json.dumps({'message': 'Invalid data sent, please send using JSON'})
            return self.render_to_response(error_data, status=400)

        passed_data = json.loads(request.body)
        passed_pk = passed_data.get('pk', None)
        if not passed_pk:
            error_data = json.dumps({'pk': 'This is a required field to update an item.'})
            return self.render_to_response(error_data, status=400)

        obj = self.get_object(pk=passed_pk)
        if obj is None:
            error_data = json.dumps({'message': 'Object not found'})
            return self.render_to_response(error_data, status=404)

        deleted, item_deleted = obj.delete()
        if deleted == 1:
            json_data = json.dumps({'message': 'Successfully deleted.'})
            return self.render_to_response(json_data, status=200)
        error_data = json.dumps({'message': 'Couldn\'t delete item, please try again later.'})
        return self.render_to_response(error_data, status=400)

    # def delete(self, request, *args, **kwargs):
    #     data = json.dumps({'message': 'You can not delete entire list!'})
    #     return self.render_to_response(data, status=403)
