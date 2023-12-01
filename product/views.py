from itertools import chain

from django.shortcuts import render, redirect

from product.forms import ChoicePollForm, DateTimePollForm, TierlistPollForm, RankingPollForm
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
    user = User.objects.get(id=request.session.get("user_id"))
    form = ChoicePollForm()
    if request.method == "POST":
        form = ChoicePollForm(request.POST)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.owner = user
            poll.save()
            poll.participants.add(user)
            return redirect("vote_code", poll.code)
    return render(request, "vote_create_choice.html", {
        "title": "Neue Umfrage",
        "user": user,
        "form": form,
    })


def vote_create_date(request):
    user = User.objects.get(id=request.session.get("user_id"))
    form = DateTimePollForm()
    if request.method == "POST":
        form = DateTimePollForm(request.POST)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.owner = user
            poll.save()
            poll.participants.add(user)
            return redirect("vote_code", poll.code)
    return render(request, "vote_create_datetime.html", {
        "title": "Neue Terminabstimmung",
        "user": user,
        "form": form,
    })


def vote_create_tierlist(request):
    user = User.objects.get(id=request.session.get("user_id"))
    form = TierlistPollForm()
    if request.method == "POST":
        form = TierlistPollForm(request.POST)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.owner = user
            poll.save()
            poll.participants.add(user)
            return redirect("vote_code", poll.code)
    return render(request, "vote_create_tierlist.html", {
        "title": "Neue Tierlist",
        "user": user,
        "form": form,
    })


def vote_create_ranking(request):
    user = User.objects.get(id=request.session.get("user_id"))
    form = RankingPollForm()
    if request.method == "POST":
        form = RankingPollForm(request.POST)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.owner = user
            poll.save()
            poll.participants.add(user)
            return redirect("vote_code", poll.code)
    return render(request, "vote_create_ranking.html", {
        "title": "Neue Rangliste",
        "user": user,
        "form": form,
    })


def vote_code(request, code):
    return render(request, "base.html", {
        "title": "Abstimmung",
    })


def log(request):
    return render(request, "base.html", {
        "title": "Meine Abstimmungen",
    })
