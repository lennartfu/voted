from django.contrib import auth
from django.shortcuts import render, redirect
from django.utils.timezone import now, timedelta

from product.forms import *
from product.models import *


def home(request):
    if request.method == "POST":
        if code := request.POST.get("code"):
            return redirect("vote_code", code)
    # get user
    user = User.objects.get(id=request.session.get("user_id"))
    # get the last polls the user viewed
    poll_views = PollView.objects.filter(user=user).order_by("-last_updated")[:8]
    last_viewed_polls = [view.poll for view in poll_views]
    return render(request, "home.html", {
        "title": "Home",
        "is_authenticated": request.user.is_authenticated,
        "user": user,
        "polls": last_viewed_polls,
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
        "is_authenticated": request.user.is_authenticated,
        "form": form,
    })


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect("home")


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
        "is_authenticated": request.user.is_authenticated,
        "form": form,
    })


def get_stats(user):
    # get all created polls
    created_polls = user.polls_created.all()
    # get amount of created polls
    num_created = len(created_polls)
    # get amount of participations in polls
    num_votes = len(user.polls_participated.all())
    # get favorite poll type
    poll_types = [("POLL", "Umfrage"), ("DATE", "Termin"), ("TIER", "Tierlist"), ("RANK", "Rangliste")]
    num_created_by_type = [len(created_polls.filter(poll_type=poll_type[0])) for poll_type in poll_types]
    index = num_created_by_type.index(max(num_created_by_type))
    favorite = poll_types[index][1]
    return num_created, num_votes, favorite


def profile(request):
    if not request.user.is_authenticated:
        return redirect("login")
    user = User.objects.get(id=request.session.get("user_id"))
    # get stats
    num_created, num_votes, favorite = get_stats(user)
    # TODO: Achievements
    return render(request, "profile_view.html", {
        "title": "Profil",
        "is_authenticated": request.user.is_authenticated,
        "user": request.user,
        "num_created": num_created,
        "num_votes": num_votes,
        "favorite": favorite,
    })


def profile_edit(request):
    if not request.user.is_authenticated:
        return redirect("login")
    user = User.objects.get(id=request.session.get('user_id'))
    # get stats
    num_created, num_votes, favorite = get_stats(user)
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
        "is_authenticated": request.user.is_authenticated,
        "form": form,
        "user": request.user,
        "num_created": num_created,
        "num_votes": num_votes,
        "favorite": favorite,
    })


def settings(request):
    return render(request, "base.html", {
        "title": "Einstellungen",
        "is_authenticated": request.user.is_authenticated,
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
    poll.save()
    return poll


def save_options(poll, form):
    options = {}
    # extract voting options from form data
    for field_name, field_value in form.cleaned_data.items():
        print(field_name, field_value)
        if field_name.startswith("option_") and field_value:
            i = field_name.split("_")[1]
            if i not in options:
                options[i] = {}
            # add value to options dict
            if field_name.endswith("_text"):
                options[i].update({"text": field_value})
            if field_name.endswith("_date"):
                options[i].update({"date": field_value})
            if field_name.endswith("_time"):
                options[i].update({"time": field_value})
            if field_name.endswith("_image"):
                options[i].update({"image": field_value})
    # create VotingOption objects
    for o in options.values():
        voting_option = VotingOption(poll=poll)
        if text := o.get("text"):
            voting_option.text = text
        if date := o.get("date"):
            voting_option.date = date
        if time := o.get("time"):
            voting_option.time = time
        if image := o.get("image"):
            voting_option.image = image
        voting_option.save()


def vote_create(request, poll_type, template, title):
    user = User.objects.get(id=request.session.get("user_id"))
    form = PollForm()
    if request.method == "POST":
        form = PollForm(request.POST, request.FILES)
        if form.is_valid():
            # save poll to database
            poll = save_poll(user, form)
            # save voting options to database
            save_options(poll, form)
            return redirect("vote_code", poll.code)
    return render(request, template, {
        "title": title,
        "is_authenticated": request.user.is_authenticated,
        "poll_type": poll_type,
        "user": user,
        "form": form,
    })


def vote_create_choice(request):
    return vote_create(request, "POLL", "vote_create_choice.html", "Neue Umfrage")


def vote_create_date(request):
    return vote_create(request, "DATE", "vote_create_datetime.html", "Neue Terminabstimmung")


def vote_create_tierlist(request):
    return vote_create(request, "TIER", "vote_create_tierlist.html", "Neue Tierlist")


def vote_create_ranking(request):
    return vote_create(request, "RANK", "vote_create_ranking.html", "Neue Rangliste")


def save_vote(poll, user, form):
    # create an object to store the vote data
    vote_data = {}
    for field_name, field_value in form.cleaned_data.items():
        if field_name.startswith("option_"):
            # add option to vote data
            option_id = int(field_name.split("_")[1])
            vote_data[option_id] = field_value
    # save vote to database
    Vote(poll=poll, user=user, data=vote_data).save()


def label_for_option(option):
    if option.poll.poll_type in ["POLL", "TIER", "RANK"]:
        return option.text
    if option.poll.poll_type == "DATE":
        locale.setlocale(locale.LC_ALL, "de_DE")
        if option.poll.date_mode == "DATE":
            return f"{option.date.strftime('%A, %d. %B %Y')}"
        if option.poll.date_mode == "TIME":
            return f"{option.time.strftime('%H:%M')} Uhr"
        if option.poll.date_mode == "BOTH":
            return f"{option.date.strftime('%A, %d.%m.%Y')} um {option.time.strftime('%H:%M')} Uhr"
        locale.setlocale(locale.LC_ALL, "en_US")


def get_result(poll):
    votes = Vote.objects.filter(poll=poll)
    voting_options = VotingOption.objects.filter(poll=poll)
    votes_per_option = {str(option.id): [label_for_option(option), 0] for option in voting_options}
    for vote in votes:
        for id, value in vote.data.items():
            option_label = label_for_option(voting_options.get(id=id))
            if not votes_per_option.get(id):
                votes_per_option[id] = [option_label, 0]
            if value:
                votes_per_option[id][1] += 1
    return sorted(votes_per_option.items(), key=lambda item: item[1][1], reverse=True)


def vote_code(request, code):
    # check if a poll with the given code exists
    if not (poll := Poll.objects.filter(code=code).first()):
        # TODO: 404 page
        return redirect("home")
    user = User.objects.get(id=request.session.get("user_id"))
    # update poll views
    if not (poll_view := PollView.objects.filter(poll=poll, user=user).first()):
        poll_view = PollView(user=user, poll=poll)
    poll_view.save()
    # handle tierlist
    if poll.poll_type == "TIER":
        return vote_code_tierlist(request, poll)
    # get poll_type
    poll_type = poll.poll_type
    if poll_type == "DATE":
        poll_type = poll.date_mode
    # get voting options for this poll and create a VotingForm
    voting_options = VotingOption.objects.filter(poll=poll)
    form = VotingForm(voting_options=voting_options, poll_type=poll_type)
    show_form = False
    # check if the user has already submitted a vote for this poll
    if not Vote.objects.filter(poll=poll, user=user).exists():
        # user has not voted yet
        show_form = True
        if request.method == "POST":
            form = VotingForm(request.POST, voting_options=voting_options)
            if form.is_valid():
                save_vote(poll, user, form)
                show_form = False
                return redirect("vote_code", poll.code)
    result = None
    if poll.show_result:
        result = get_result(poll)
    is_owner = poll.owner == user
    return render(request, "vote_code.html", {
        "title": poll.title,
        "is_authenticated": request.user.is_authenticated,
        "is_owner": is_owner,
        "show_form": show_form,
        "form": form,
        "poll": poll,
        "result": result,
    })


def vote_code_tierlist(request, poll):
    user = User.objects.get(id=request.session.get("user_id"))
    voting_options = VotingOption.objects.filter(poll=poll)
    show_form = False
    # check if the user has already submitted a vote for this poll
    if not Vote.objects.filter(poll=poll, user=user).exists():
        # user has not voted yet
        show_form = True
    return render(request, "vote_code_tierlist.html", {
        "title": poll.title,
        "is_authenticated": request.user.is_authenticated,
        "show_form": show_form,
        "voting_options": voting_options,
        "poll": poll,
    })


def vote_close(request, code):
    # check if a poll with the given code exists
    if not (poll := Poll.objects.filter(code=code).first()):
        # TODO: 404 page
        return redirect("home")
    user = User.objects.get(id=request.session.get("user_id"))
    if user == poll.owner:
        # user is the poll owner
        poll.timestamp_end = now()
        poll.is_active = False
        poll.show_result = True
        poll.save()
    return redirect("vote_code", code)


def log(request):
    return render(request, "base.html", {
        "title": "Meine Abstimmungen",
        "is_authenticated": request.user.is_authenticated,
    })
