from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    path("profile/edit", views.profile_edit, name="profile_edit"),
    path("settings", views.settings, name="settings"),
    path("vote/create/choice", views.vote_create_choice, name="vote_create_choice"),
    path("vote/create/date", views.vote_create_date, name="vote_create_date"),
    path("vote/create/tierlist", views.vote_create_tierlist, name="vote_create_tierlist"),
    path("vote/create/ranking", views.vote_create_ranking, name="vote_create_ranking"),
    path("vote/<str:code>", views.vote_code, name="vote_code"),
    path("vote/<str:code>/close", views.vote_close, name="vote_close"),
    path("log", views.log, name="log"),
    path("<path:resource>", views.catch_all, name="catch_all"),
]
