import locale

from django import forms
from django.contrib.auth.forms import UserCreationForm

from product.models import *


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label="Benutzername:")
    password = forms.CharField(widget=forms.PasswordInput, label="Passwort:")


class RegisterForm(UserCreationForm):
    class Meta:
        model = DjangoUser
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

    username = forms.CharField(max_length=50, label="Benutzername:")
    first_name = forms.CharField(max_length=50, label="Vorname:")
    last_name = forms.CharField(max_length=50, label="Nachname:")
    email = forms.EmailField(label="Email:")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Passwort:")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Passwort bestätigen:")


class UserForm(forms.ModelForm):
    class Meta:
        model = DjangoUser
        fields = ["first_name", "last_name", "username", "email"]

    first_name = forms.CharField(required=False, disabled=True, max_length=50, label="Vorname:")
    last_name = forms.CharField(required=False, disabled=True, max_length=50, label="Nachname:")
    username = forms.CharField(max_length=50, label="Benutzername:")
    email = forms.EmailField(label="Email:")
    password1 = forms.CharField(required=False, widget=forms.PasswordInput, label="Neues Passwort:")
    password2 = forms.CharField(required=False, widget=forms.PasswordInput, label="Passwort bestätigen:")


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = [
            "poll_type",
            "title",
            "description",
            "password",
            "show_result",
            "logged_in_only",
            "multiple_choice_allowed",
            "custom_answers_allowed",
            "date_mode",
            "num_tiers",
            "criteria_good",
            "criteria_bad",
        ]

    # poll type
    TYPE_CHOICES = (
        ("POLL", "Umfrage"),
        ("DATE", "Terminabstimmung"),
        ("TIER", "Tierlist"),
        ("RANK", "Rangliste"),
    )
    poll_type = forms.ChoiceField(choices=TYPE_CHOICES)
    # basic attributes
    title = forms.CharField(max_length=50, label="Titel:")
    description = forms.CharField(required=False, max_length=500, widget=forms.Textarea, label="Beschreibung:")
    password = forms.CharField(required=False, label="Passwort:")
    days = forms.IntegerField(required=False, min_value=0, max_value=365, label="Tage:")
    hours = forms.IntegerField(required=False, min_value=0, max_value=24, label="Stunden:")
    minutes = forms.IntegerField(required=False, min_value=0, max_value=60, label="Minuten:")
    # extra options
    show_result = forms.BooleanField(required=False, label="Ergebnis anzeigen:")
    logged_in_only = forms.BooleanField(required=False, label="Nur für angemeldete Nutzer:")
    multiple_choice_allowed = forms.BooleanField(required=False, label="Mehrfachauswahl:")
    custom_answers_allowed = forms.BooleanField(required=False, label="Eigene Antworten erlaubt:")
    # date poll options
    DATE_MODE_CHOICES = (
        ("DATE", "Datum"),
        ("TIME", "Uhrzeit"),
        ("BOTH", "Datum & Uhrzeit"),
    )
    date_mode = forms.ChoiceField(required=False, choices=DATE_MODE_CHOICES, initial="DATE", label="Modus:")
    # tierlist poll options
    num_tiers = forms.IntegerField(required=False, min_value=2, max_value=6, initial=6, label="Tiers:")
    # ranking poll options
    criteria_good = forms.CharField(required=False, max_length=50, label="von:", initial="gut")
    criteria_bad = forms.CharField(required=False, max_length=50, label="bis:", initial="schlecht")

    def __init__(self, *args, **kwargs):
        # the maximum number of voting options a user can add to this poll; defaults to 20
        max_options = kwargs.pop("max_options", 20)
        super(PollForm, self).__init__(*args, **kwargs)
        # for each option, add text, date, time and image fields
        for i in range(max_options):
            self.fields[f"option_{i + 1}_text"] = forms.CharField(required=False, max_length=50, label=f"Text:")
            self.fields[f"option_{i + 1}_date"] = forms.DateField(required=False, label=f"Datum:", localize=True)
            self.fields[f"option_{i + 1}_time"] = forms.TimeField(required=False, label=f"Uhrzeit:", localize=True)
            self.fields[f"option_{i + 1}_image"] = forms.ImageField(required=False, label=f"Bild:")


class VotingForm(forms.Form):
    def __init__(self, *args, **kwargs):
        poll_type = kwargs.pop("poll_type", "POLL")
        # get voting options
        voting_options = kwargs.pop("voting_options", ())
        super(VotingForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""
        # for each option, add a boolean field
        locale.setlocale(locale.LC_ALL, "de_DE")
        for o in voting_options:
            if poll_type == "POLL":
                self.fields[f"option_{o.id}"] = forms.BooleanField(required=False, label=o.text)
            if poll_type == "DATE":
                label = f"{o.date.strftime('%A, %d. %B %Y')}"
                self.fields[f"option_{o.id}"] = forms.BooleanField(required=False, label=label)
            if poll_type == "TIME":
                label = f"{o.time.strftime('%H:%M')} Uhr"
                self.fields[f"option_{o.id}"] = forms.BooleanField(required=False, label=label)
            if poll_type == "BOTH":
                label = f"{o.date.strftime('%A, %d.%m.%Y')} um {o.time.strftime('%H:%M')} Uhr"
                self.fields[f"option_{o.id}"] = forms.BooleanField(required=False, label=label)
            if poll_type == "TIER":
                self.fields[f"option_{o.id}"] = forms.BooleanField(required=False, label=o.image)
            if poll_type == "RANK":
                self.fields[f"option_{o.id}"] = forms.BooleanField(required=False, label=o.text)
        locale.setlocale(locale.LC_ALL, "en_US")
