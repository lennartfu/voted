from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    path("profile/edit", views.profile_edit, name="profile_edit"),
    path("settings", views.settings, name="settings"),
    path("vote/create", views.vote_create, name="vote_create"),
    path("vote/<int:code>", views.vote_code, name="vote_code"),
    path("log", views.log, name="log"),
]
