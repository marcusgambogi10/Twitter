from django.urls import path
from .views import PostDetail, PostList, create_post

urlpatterns = [
    path("", PostList.as_view(), name="home"),
    path("home/create/", create_post, name="create_post"),
    path("home/<slug:slug>/", PostDetail.as_view(), name="post_detail"),
]
