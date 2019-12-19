from rest_framework import serializers
from rest_framework.reverse import reverse

from accounts.api.serializers import UserPublicSerializer
from status.models import Status


class StatusSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = Status
        fields = [
            'uri',
            'id',
            'user',
            'content',
            'image'
        ]
        read_only_fields = ['user']

    def get_uri(self, obj):
        request = self.context.get('request')
        return reverse('api-status:detail', kwargs={'pk': obj.pk}, request=request)

    # def validate_content(self, value):
    #     if len(value) > 240:
    #         raise serializers.ValidationError('This is way too long!')
    #     return value

    def validate(self, data):
        content = data.get('content', None)
        if content == '':
            content = None
        image = data.get('image', None)
        if content is None and image is None:
            raise serializers.ValidationError('Content or image is required!')
        return data


class StatusInlineUserSerializer(StatusSerializer):
    # uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Status
        fields = [
            'uri',
            'id',
            'content',
            'image'
        ]

    # def get_uri(self, obj):
    #     return f'/api/status/{obj.id}'

# class StatusInlineUserSerializer(serializers.ModelSerializer):
#     uri = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = Status
#         fields = [
#             'uri',
#             'id',
#             'content',
#             'image'
#         ]

#     def get_uri(self, obj):
#         request = self.context.get('request')
#         return reverse('api-status:detail', kwargs={'pk': obj.pk}, request=request)
