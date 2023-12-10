from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

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


class ChoicePollForm(forms.ModelForm):
    class Meta:
        model = ChoicePoll
        fields = [
            "title",
            "description",
            "password",
            "show_result",
            "logged_in_only",
            "multiple_choice_allowed",
            "custom_answers_allowed",
        ]

    # basic fields
    title = forms.CharField(max_length=50, label="Titel:")
    description = forms.CharField(required=False, max_length=500, widget=forms.Textarea, label="Beschreibung:")
    password = forms.CharField(required=False, label="Passwort:")
    days = forms.IntegerField(required=False, min_value=0, max_value=365, label="Tage:")
    hours = forms.IntegerField(required=False, min_value=0, max_value=24, label="Stunden:")
    minutes = forms.IntegerField(required=False, min_value=0, max_value=60, label="Minuten:")
    # extra options
    show_result = forms.BooleanField(required=False, label="Ergebnis anzeigen:")
    logged_in_only = forms.BooleanField(required=False, label="Nur für angemeldete Nutzer:")
    # type-specific options
    multiple_choice_allowed = forms.BooleanField(required=False, label="Mehrfachauswahl:")
    custom_answers_allowed = forms.BooleanField(required=False, label="Eigene Antworten erlaubt:")
    # voting items; the first 2 are required
    item_1 = forms.CharField(max_length=50, label="Antwort:")
    item_2 = forms.CharField(max_length=50, label="Antwort:")

    def __init__(self, *args, **kwargs):
        # the maximum number of items a user can add to this poll; defaults to 10
        max_items = kwargs.pop("max_items", 20)
        super(ChoicePollForm, self).__init__(*args, **kwargs)
        # add extra item fields
        for i in range(2, max_items):
            self.fields[f"item_{i + 1}"] = forms.CharField(required=False, max_length=50,
                                                           label=f"Antwort:")


class DateTimeLocalInput(forms.DateTimeInput):
    input_type = "datetime-local"


class DateTimeLocalField(forms.DateTimeField):
    input_formats = [
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M"
    ]
    widget = DateTimeLocalInput(format="%Y-%m-%dT%H:%M")


class DateTimePollForm(forms.ModelForm):
    class Meta:
        model = DateTimePoll
        fields = [
            "title",
            "description",
            "password",
            "show_result",
            "logged_in_only",
            "mode",
            "multiple_choice_allowed",
        ]

    # basic fields
    title = forms.CharField(max_length=50, label="Titel:")
    description = forms.CharField(required=False, max_length=500, widget=forms.Textarea, label="Beschreibung:")
    password = forms.CharField(required=False, label="Passwort:")
    days = forms.IntegerField(required=False, min_value=0, max_value=365, label="Tage:")
    hours = forms.IntegerField(required=False, min_value=0, max_value=24, label="Stunden:")
    minutes = forms.IntegerField(required=False, min_value=0, max_value=60, label="Minuten:")
    # extra options
    show_result = forms.BooleanField(required=False, label="Ergebnis anzeigen:")
    logged_in_only = forms.BooleanField(required=False, label="Nur für angemeldete Nutzer:")
    # type-specific options
    mode = forms.ChoiceField(choices=(
        ("DAT", "Datum"),
        ("UHR", "Uhrzeit"),
        ("D&U", "Datum & Uhrzeit"),
    ), initial="D&U", label="Modus:")
    multiple_choice_allowed = forms.BooleanField(required=False, label="Mehrfachauswahl:")
    # voting items; the first 2 are required
    item_1 = DateTimeLocalField(label="Antwort:")
    item_2 = DateTimeLocalField(label="Antwort:")

    def __init__(self, *args, **kwargs):
        # the maximum number of items a user can add to this poll; defaults to 10
        max_items = kwargs.pop("max_items", 20)
        super(DateTimePollForm, self).__init__(*args, **kwargs)
        # add extra item fields
        for i in range(2, max_items):
            self.fields[f"item_{i + 1}"] = DateTimeLocalField(required=False, label=f"Antwort:")


class TierlistPollForm(forms.ModelForm):
    class Meta:
        model = TierlistPoll
        fields = [
            "title",
            "description",
            "password",
            "show_result",
            "logged_in_only",
            "num_tiers",
        ]

    # basic fields
    title = forms.CharField(max_length=50, label="Titel:")
    description = forms.CharField(required=False, max_length=500, widget=forms.Textarea, label="Beschreibung:")
    password = forms.CharField(required=False, label="Passwort:")
    days = forms.IntegerField(required=False, min_value=0, max_value=365, label="Tage:")
    hours = forms.IntegerField(required=False, min_value=0, max_value=24, label="Stunden:")
    minutes = forms.IntegerField(required=False, min_value=0, max_value=60, label="Minuten:")
    # extra options
    show_result = forms.BooleanField(required=False, label="Ergebnis anzeigen:")
    logged_in_only = forms.BooleanField(required=False, label="Nur für angemeldete Nutzer:")
    # type-specific options
    num_tiers = forms.IntegerField(label="Tiers:", min_value=2, max_value=6, step_size=1, initial=6)
    # voting items; the first 2 are required
    item_1 = forms.ImageField(label="Antwort:")
    item_2 = forms.ImageField(label="Antwort:")

    def __init__(self, *args, **kwargs):
        # the maximum number of items a user can add to this poll; defaults to 10
        max_items = kwargs.pop("max_items", 20)
        super(TierlistPollForm, self).__init__(*args, **kwargs)
        # add extra item fields
        for i in range(2, max_items):
            self.fields[f"item_{i + 1}"] = forms.ImageField(required=False, label=f"Antwort:")


class RankingPollForm(forms.ModelForm):
    class Meta:
        model = RankingPoll
        fields = [
            "title",
            "description",
            "password",
            "show_result",
            "logged_in_only",
            "criteria_good",
            "criteria_bad",
        ]

    # Basic fields
    title = forms.CharField(max_length=50, label="Titel:")
    description = forms.CharField(required=False, max_length=500, widget=forms.Textarea, label="Beschreibung:")
    password = forms.CharField(required=False, label="Passwort:")
    days = forms.IntegerField(required=False, min_value=0, max_value=365, label="Tage:")
    hours = forms.IntegerField(required=False, min_value=0, max_value=24, label="Stunden:")
    minutes = forms.IntegerField(required=False, min_value=0, max_value=60, label="Minuten:")
    # extra options
    show_result = forms.BooleanField(required=False, label="Ergebnis anzeigen:")
    logged_in_only = forms.BooleanField(required=False, label="Nur für angemeldete Nutzer:")
    # type-specific options
    criteria_good = forms.CharField(max_length=50, label="von:", initial="gut")
    criteria_bad = forms.CharField(max_length=50, label="bis:", initial="schlecht")
    # voting items; the first 2 are required
    item_1 = forms.ImageField(label="Antwort:")
    item_2 = forms.ImageField(label="Antwort:")

    def __init__(self, *args, **kwargs):
        # the maximum number of items a user can add to this poll; defaults to 10
        max_items = kwargs.pop("max_items", 20)
        super(RankingPollForm, self).__init__(*args, **kwargs)
        # add extra item fields
        for i in range(2, max_items):
            self.fields[f"item_{i + 1}"] = forms.ImageField(required=False, label=f"Antwort:")


class ChoiceVoteForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # get vote objects
        vote_objects = kwargs.pop("vote_objects", None)
        super(ChoiceVoteForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""
        # add vote object fields
        if vote_objects:
            for o in vote_objects:
                self.fields[f"object_{o.id}"] = forms.BooleanField(required=False, label=o.value)


class DateTimeVoteForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # get vote objects
        vote_objects = kwargs.pop("vote_objects", None)
        super(DateTimeVoteForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""
        # add vote object fields
        if vote_objects:
            for o in vote_objects:
                self.fields[f"object_{o.id}"] = forms.BooleanField(required=False, label=o.value)
