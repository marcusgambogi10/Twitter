from django import forms
from django.utils.text import slugify

from .models import Post


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "status", "content"]

    def save(self, commit=True):
        instance = super(CreatePostForm, self).save(commit=False)
        instance.slug = slugify(instance.title)
        if commit:
            instance.save()
        return instance
