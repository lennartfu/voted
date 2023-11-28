from itertools import chain

from django.shortcuts import render

from product.models import User


def home(request):
    user_id = request.session.get("user_id")
    if not user_id:
        # create user
        user = User.objects.create()
        user_id = user.id
        request.session["user_id"] = str(user_id)
    else:
        # get existing user
        user = User.objects.get(id=user_id)
    # get 4 newest participated polls
    choice_polls = user.product_choicepoll_participated.all().order_by("-created_date")
    datetime_polls = user.product_datetimepoll_participated.all().order_by("-created_date")
    tierlist_polls = user.product_tierlistpoll_participated.all().order_by("-created_date")
    ranking_polls = user.product_rankingpoll_participated.all().order_by("-created_date")
    # sort polls
    polls = list(chain(choice_polls, datetime_polls, tierlist_polls, ranking_polls))
    sorted_polls = sorted(polls, key=lambda poll: poll.created_date, reverse=True)[:4]
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


def vote_create(request):
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
