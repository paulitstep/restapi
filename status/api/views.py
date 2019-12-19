import json

from django.shortcuts import get_object_or_404

from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView
)
from rest_framework.mixins import (
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
)
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.api.permissions import IsOwnerOrReadOnly
from status.models import Status

from .serializers import StatusSerializer


def is_json(json_data):
    try:
        real_json = json.loads(json_data)
        is_valid = True
    except ValueError:
        is_valid = False
    return is_valid


class StatusAPIView(
        CreateModelMixin,
        ListAPIView):  # Create & List
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = StatusSerializer
    passed_pk = None
    search_fields = ('user__username', 'content')
    ordering_fields = ('user__username', 'timestamp')
    queryset = Status.objects.all()

    # def get_queryset(self):
    #     request = self.request
    #     qs = Status.objects.all()
    #     query = request.GET.get('q')
    #     if query is not None:
    #         qs = qs.filter(content__icontains=query)
    #     return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StatusAPIDetailView(UpdateModelMixin, DestroyModelMixin, RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]
    serializer_class = StatusSerializer
    queryset = Status.objects.all()
    lookup_field = 'pk'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# class StatusAPIView(CreateModelMixin, ListAPIView):  # Create & List
#     permission_classes = []
#     authentication_classes = []
#     serializer_class = StatusSerializer
#     passed_pk = None

#     def get_queryset(self):
#         qs = Status.objects.all()
#         query = self.request.GET.get('q')
#         if query is not None:
#             qs = qs.filter(content__icontains=query)
#         return qs

#     def get_object(self):
#         passed_pk = self.request.GET.get('pk', None) or self.passed_pk
#         queryset = self.get_queryset()
#         obj = None
#         if passed_pk is not None:
#             obj = get_object_or_404(queryset, pk=passed_pk)
#             self.check_object_permissions(self.request, obj)
#         return obj

#     def get(self, request, *args, **kwargs):
#         url_passed_pk = request.GET.get('pk', None)
#         json_data = {}
#         body = request.body
#         if is_json(body):
#             json_data = json.loads(request.body)
#         new_passed_pk = json_data.get('id', None)
#         passed_pk = url_passed_pk or new_passed_pk or None
#         self.passed_pk = passed_pk
#         if passed_pk is not None:
#             return self.retrieve(request, *args, **kwargs)
#         return super().get(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         url_passed_pk = request.GET.get('pk', None)
#         json_data = {}
#         body = request.body
#         if is_json(body):
#             json_data = json.loads(request.body)
#         new_passed_pk = json_data.get('id', None)
#         passed_pk = url_passed_pk or new_passed_pk or None
#         self.passed_pk = passed_pk
#         return self.update(request, *args, **kwargs)

#     def patch(self, request, *args, **kwargs):
#         url_passed_pk = request.GET.get('pk', None)
#         json_data = {}
#         body = request.body
#         if is_json(body):
#             json_data = json.loads(request.body)
#         new_passed_pk = json_data.get('id', None)
#         passed_pk = url_passed_pk or new_passed_pk or None
#         self.passed_pk = passed_pk
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         url_passed_pk = request.GET.get('pk', None)
#         json_data = {}
#         body = request.body
#         if is_json(body):
#             json_data = json.loads(request.body)
#         new_passed_pk = json_data.get('id', None)
#         passed_pk = url_passed_pk or new_passed_pk or None
#         self.passed_pk = passed_pk
#         return self.destroy(request, *args, **kwargs)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


# class StatusListSearchAPIView(APIView):
#     permission_classes = []
#     authentication_classes = []

#     def get(self, request, format=None):
#         qs = Status.objects.all()
#         serializer = StatusSerializer(qs, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         qs = Status.objects.all()
#         serializer = StatusSerializer(qs, many=True)
#         return Response(serializer.data)


# class StatusAPIView(CreateModelMixin, ListAPIView):  # Create & List View
#     permission_classes = []
#     authentication_classes = []
#     serializer_class = StatusSerializer

#     def get_queryset(self):
#         qs = Status.objects.all()
#         query = self.request.GET.get('q')
#         if query is not None:
#             qs = qs.filter(content__icontains=query)
#         return qs

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


# class StatusDetailAPIView(UpdateModelMixin, DestroyModelMixin, RetrieveAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Status.objects.all()
#     serializer_class = StatusSerializer

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


# class StatusUpdateAPIView(UpdateAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Status.objects.all()
#     serializer_class = StatusSerializer


# class StatusDeleteAPIView(DestroyAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Status.objects.all()
#     serializer_class = StatusSerializer
