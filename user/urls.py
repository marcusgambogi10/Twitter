from rest_framework.routers import SimpleRouter
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *

router = SimpleRouter()

router.register("user", UserViewSet, basename="user")
router.register("profile", ProfileViewSet, basename="profile")


urlpatterns = [
    path("users/", all_users, name="all-users"),
    path("users/profile/<int:id>/", ProfileView.as_view(), name="user_profile"),
    path("update_bio/", update_bio, name="update_bio"),
    path(
        "login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"
    ),
    path("signup/", signup, name="signup"),
    path("logout/", logout_view, name="logout"),
]

urlpatterns += router.urls
