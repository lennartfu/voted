from itertools import chain

from django.contrib import auth
from django.shortcuts import render, redirect
from django.utils.timezone import now, timedelta

from product.forms import ChoicePollForm, DateTimePollForm, TierlistPollForm, RankingPollForm, LoginForm, UserForm
from product.models import User, ChoiceObject, DateTimeObject, TierlistObject, RankingObject


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
    # redirect to profile if user is already logged in
    if request.user.is_authenticated:
        return redirect("profile")
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            # authenticate credentials
            account = auth.authenticate(request, username=username, password=password)
            if account is not None:
                # log user in and redirect to profile
                auth.login(request, account)
                return redirect("profile")
            else:
                form.add_error("username", "Ungültige Logindaten. Bitte erneut probieren.")
    return render(request, "login.html", {
        "title": "Login",
        "form": form,
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
    if not request.user.is_authenticated:
        return redirect("login")
    form = UserForm(instance=request.user)
    if request.method == "POST":
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    return render(request, "profile_edit.html", {
        "title": "Profil bearbeiten",
        "form": form,
    })


def settings(request):
    return render(request, "base.html", {
        "title": "Einstellungen",
    })


def save_poll(user, form):
    poll = form.save(commit=False)
    poll.owner = user
    # convert days, hours, minutes to int; set to 0 if None
    days = int(form.cleaned_data.get("days") or 0)
    hours = int(form.cleaned_data.get("hours") or 0)
    minutes = int(form.cleaned_data.get("minutes") or 0)
    # set timestamp_end if a value was provided
    if days or hours or minutes:
        poll.timestamp_end = now() + timedelta(days=days, hours=hours, minutes=minutes)
    # save poll to database
    poll.save()
    poll.participants.add(user)
    return poll


def vote_create_choice(request):
    user = User.objects.get(id=request.session.get("user_id"))
    form = ChoicePollForm()
    if request.method == "POST":
        form = ChoicePollForm(request.POST)
        if form.is_valid():
            poll = save_poll(user, form)
            # get items from form; create a ChoiceObject for each
            for field_name, field_value in form.cleaned_data.items():
                if field_name.startswith("item_") and field_value:
                    ChoiceObject(poll=poll, value=field_value).save()
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
            poll = save_poll(user, form)
            # get items from form; create a DateTimeObject for each
            for field_name, field_value in form.cleaned_data.items():
                if field_name.startswith("item_") and field_value:
                    DateTimeObject(poll=poll, value=field_value).save()
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
        form = TierlistPollForm(request.POST, request.FILES)
        if form.is_valid():
            poll = save_poll(user, form)
            # get items from form; create a TierlistObject for each
            for field_name, field_value in form.cleaned_data.items():
                if field_name.startswith("item_") and field_value:
                    # TODO: upload/save image
                    TierlistObject(poll=poll, image=field_value, value=field_value).save()
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
        form = RankingPollForm(request.POST, request.FILES)
        if form.is_valid():
            poll = save_poll(user, form)
            # get items from form; create a RankingObject for each
            for field_name, field_value in form.cleaned_data.items():
                if field_name.startswith("item_") and field_value:
                    # TODO: upload/save image
                    RankingObject(poll=poll, image=field_value, value=field_value).save()
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
