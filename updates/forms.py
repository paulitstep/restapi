from django import forms

from .models import Update


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Update
        fields = [
            'user',
            'content',
            'image'
        ]

    def clean(self, *args, **kwargs):
        data = self.cleaned_data
        content = data.get('content', None)
        if content == '':
            content = None
        image = data.get('image', None)
        if content is None and image is None:
            raise forms.ValidationError('content or image is required!')
        return super().clean(*args, **kwargs)
