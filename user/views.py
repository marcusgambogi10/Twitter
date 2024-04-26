from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from django.contrib.auth import get_user_model, login, authenticate, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader


from .models import Profile
from .serializers import ProfileSerializer, UserSerializer
from .forms import RegistrationForm, UpdateBioForm

from post.models import Post


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    lookup_field = "id"
    serializer_class = ProfileSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "profile.html"

    def get(self, request, id):
        profile = Profile.objects.get(id=id)
        user_id = self.kwargs.get("id")
        user = profile.user
        user_posts = Post.objects.filter(author=profile.user).order_by("-created_on")
        return Response(
            {
                "profile": profile,
                "user": user,
                "user_posts": user_posts,
            }
        )

    def post(self, request, id):
        profile = Profile.objects.get(id=id)
        user_posts = Post.objects.filter(author=profile.user).order_by("-created_on")

        bio_form = UpdateBioForm(request.POST, instance=profile)
        if bio_form.is_valid():
            bio_form.save()

        return Response(
            {"profile": profile, "user_posts": user_posts, "bio_form": bio_form}
        )


def update_bio(request):
    if request.method == "POST":
        profile_id = request.POST.get("profile_id")
        new_bio = request.POST.get("new_bio")

        profile = Profile(id=profile_id)
        profile.bio = new_bio
        profile.save()

        return JsonResponse({"success": True})

    return JsonResponse({"success": False})


def all_users(request):
    users = get_user_model().objects.all().values()
    template = loader.get_template("all_users.html")
    context = {
        "users": users,
    }
    return HttpResponse(template.render(context, request))


def signup(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("/")
    else:
        form = RegistrationForm()
    return render(request, "registration/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("/login/")
