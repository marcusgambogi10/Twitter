from django.test import TestCase
from django.template.defaultfilters import slugify
from project.models import Post


class ModelsTestCase(TestCase):
    def test_post_has_slug(self):
        """Posts are given slugs correctly when saving"""
        post = Post.objects.create(title="Post")

        post.author = "Marcus Gambogi"
        post.save()
        self.assertEqual(post.slug, slugify(post.title))