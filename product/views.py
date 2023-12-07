from itertools import chain

from django.contrib import auth
from django.shortcuts import render, redirect
from django.utils.timezone import now, timedelta

from product.forms import *
from product.models import *


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
    # redirect to profile if user is already logged in
    if request.user.is_authenticated:
        return redirect("profile")
    # get user
    user = User.objects.get(id=request.session.get("user_id"))
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # create account
            account = form.save()
            # add account to existing user
            user.account = account
            user.save()
            # log user in and redirect to profile
            auth.login(request, account)
            return redirect("profile")
    return render(request, "register.html", {
        "title": "Registrierung",
        "form": form,
    })


def profile(request):
    if not request.user.is_authenticated:
        return redirect("login")
    # get user
    user = User.objects.get(id=request.session.get("user_id"))
    # get all created polls
    choice_polls = user.product_choicepolls_created.all()
    datetime_polls = user.product_datetimepolls_created.all()
    tierlist_polls = user.product_tierlistpolls_created.all()
    ranking_polls = user.product_rankingpolls_created.all()
    # get number of created polls
    num_created = len(list(chain(choice_polls, datetime_polls, tierlist_polls, ranking_polls)))
    # get all participated polls
    choice_polls = user.product_choicepolls_participated.all()
    datetime_polls = user.product_datetimepolls_participated.all()
    tierlist_polls = user.product_tierlistpolls_participated.all()
    ranking_polls = user.product_rankingpolls_participated.all()
    # get number of votes
    num_votes = len(list(chain(choice_polls, datetime_polls, tierlist_polls, ranking_polls)))
    return render(request, "profile.html", {
        "title": "Profil",
        "user": request.user,
        "num_created": num_created,
        "num_votes": num_votes,
        "favorite": "Tierlist",
    })


def profile_edit(request):
    if not request.user.is_authenticated:
        return redirect("login")
    form = UserForm(instance=request.user)
    if request.method == "POST":
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            account = form.save(commit=False)
            password1 = form.cleaned_data.get("password1")
            password2 = form.cleaned_data.get("password2")
            # check if user wants to change password
            if not (password1 or password2):
                # save changes and redirect
                account.save()
                return redirect("profile")
            # check if passwords match
            if password1 == password2:
                # change password
                account.set_password(password1)
                account.save()
                # log user in and redirect to profile
                auth.login(request, account)
                return redirect("profile")
            else:
                # save error message to form
                form.add_error("password2", "The two password fields didn’t match.")
    return render(request, "profile_edit.html", {
        "title": "Profil bearbeiten",
        "form": form,
        "user": request.user,
        "num_created": 195,
        "num_votes": 245,
        "favorite": "Tierlist",
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
