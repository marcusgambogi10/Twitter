from django.shortcuts import render, redirect
from django.views import generic

from .models import Post
from .forms import CreatePostForm


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"


class PostDetail(generic.DetailView):
    model = Post
    template_name = "post_detail.html"


def create_post(request):
    post_form = CreatePostForm()
    if request.method == "POST":
        post_form = CreatePostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post_form.save()
            return redirect("/")
    else:
        post_form = CreatePostForm()
    context = {
        "post_form": post_form,
    }

    return render(request, "create_post.html", context=context)
