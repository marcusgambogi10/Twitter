from django.db import models
from django.contrib.auth import get_user_model
from post.models import Post


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    bio = models.TextField(
        blank=True, default="I'm using Tweeter!", max_length=360, editable=True
    )
    user_posts = models.ManyToManyField(Post)

    def __str__(self):
        return self.user.username
