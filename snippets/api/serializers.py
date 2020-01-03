from django.contrib.auth.models import User

from rest_framework import serializers

from snippets.models import Snippet


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='api-tutorial:snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = [
            'url',
            'id',
            'username',
            'snippets'
        ]
        extra_kwargs = {
            'url': {'view_name': 'api-tutorial:user-detail'},
        }


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='api-tutorial:snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = [
            'url',
            'id',
            'highlight',
            'user',
            'title',
            'code',
            'linenos',
            'language',
            'style'
        ]
        extra_kwargs = {
            'url': {'view_name': 'api-tutorial:snippet-detail'},
        }


    # id = serializers.IntegerField(read_only=True)
    # title = serializers.CharField(required=False, allow_blank=True, max_length=50)
    # code = serializers.CharField(style={'base_template': 'textarea.html'})
    # linenos = serializers.BooleanField(required=False)
    # language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    # style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    # def create(self, data):
    #     """
    #     Create and return a new 'Snippet' instance, given the data.
    #     """
    #     return Snippet.objects.create(**data)

    # def update(self, instance, data):
    #     """
    #     Update and return an existing 'Snippet' instance, given the data.
    #     """
    #     instance.title = data.get('title', instance.title)
    #     instance.code = data.get('code', instance.code)
    #     instance.linenos = data.get('linenos', instance.linenos)
    #     instance.language = data.get('language', instance.language)
    #     instance.style = data.get('style', instance.style)
    #     instance.save()
    #     return instance
