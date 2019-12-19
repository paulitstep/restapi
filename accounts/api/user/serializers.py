from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.reverse import reverse

from status.api.serializers import StatusInlineUserSerializer


class UserDetailSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'uri',
            'status'
        ]

    def get_uri(self, obj):
        request = self.context.get('request')
        return reverse('api-user:detail', kwargs={'username': obj.username}, request=request)

    def get_status(self, obj):
        request = self.context.get('request')
        qs = obj.status_set.all().order_by('-timestamp')
        data = {
            'uri': self.get_uri(obj) + 'status/',
            'last': StatusInlineUserSerializer(qs.first(), context={'request': request}).data,
            'recent': StatusInlineUserSerializer(qs[:10], many=True, context={'request': request}).data
        }
        return data
