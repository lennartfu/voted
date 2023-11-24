from django.shortcuts import render


def home(request):
    return render(request, "product/base.html", {
        "title": "Home",
    })


def login(request):
    return render(request, "product/base.html", {
        "title": "Login",
    })


def register(request):
    return render(request, "product/base.html", {
        "title": "Registrierung",
    })


def profile(request):
    return render(request, "product/base.html", {
        "title": "Profil",
    })


def profile_edit(request):
    return render(request, "product/base.html", {
        "title": "Profil bearbeiten",
    })


def settings(request):
    return render(request, "product/base.html", {
        "title": "Einstellungen",
    })


def vote_create(request):
    return render(request, "product/base.html", {
        "title": "Neue Abstimmung",
    })


def vote_code(request):
    return render(request, "product/base.html", {
        "title": "Abstimmung",
    })


def log(request):
    return render(request, "product/base.html", {
        "title": "Meine Abstimmungen",
    })
