from itertools import chain

from django.shortcuts import render

from product.models import User


def home(request):
    # get user
    user = User.objects.get(id=request.session.get("user_id"))
    # for each poll type, get the 4 latest polls the user participated in
    choice_polls = user.product_choicepolls_participated.all().order_by("-timestamp_created")
    datetime_polls = user.product_datetimepolls_participated.all().order_by("-timestamp_created")
    tierlist_polls = user.product_tierlistpolls_participated.all().order_by("-timestamp_created")
    ranking_polls = user.product_rankingpolls_participated.all().order_by("-timestamp_created")
    # create a list with all 16 polls
    polls = list(chain(choice_polls, datetime_polls, tierlist_polls, ranking_polls))
    # sort polls
    sorted_polls = sorted(polls, key=lambda poll: poll.timestamp_created, reverse=True)[:4]
    return render(request, "home.html", {
        "title": "Home",
        "user": user,
        "polls": sorted_polls,
    })


def login(request):
    return render(request, "base.html", {
        "title": "Login",
    })


def register(request):
    return render(request, "base.html", {
        "title": "Registrierung",
    })


def profile(request):
    return render(request, "base.html", {
        "title": "Profil",
    })


def profile_edit(request):
    return render(request, "base.html", {
        "title": "Profil bearbeiten",
    })


def settings(request):
    return render(request, "base.html", {
        "title": "Einstellungen",
    })


def vote_create_choice(request):
    return render(request, "base.html", {
        "title": "Neue Abstimmung",
    })


def vote_create_date(request):
    return render(request, "base.html", {
        "title": "Neue Abstimmung",
    })


def vote_create_tierlist(request):
    return render(request, "base.html", {
        "title": "Neue Abstimmung",
    })


def vote_create_ranking(request):
    return render(request, "base.html", {
        "title": "Neue Abstimmung",
    })


def vote_code(request):
    return render(request, "base.html", {
        "title": "Abstimmung",
    })


def log(request):
    return render(request, "base.html", {
        "title": "Meine Abstimmungen",
    })
