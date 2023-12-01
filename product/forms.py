from django import forms

from product.models import *


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
    description = forms.CharField(required=False, widget=forms.Textarea, label="Beschreibung:")
    password = forms.CharField(required=False, label="Passwort:")
    days = forms.IntegerField(required=False, min_value=0, max_value=65, label="Tage:")
    hours = forms.IntegerField(required=False, min_value=0, max_value=24, label="Stunden:")
    minutes = forms.IntegerField(required=False, min_value=0, max_value=60, label="Minuten:")
    # extra options
    show_result = forms.BooleanField(required=False, label="Ergebnis anzeigen:")
    logged_in_only = forms.BooleanField(required=False, label="Nur für angemeldete Nutzer:")
    # type-specific options
    multiple_choice_allowed = forms.BooleanField(required=False, label="Mehrfachauswahl möglich:")
    custom_answers_allowed = forms.BooleanField(required=False, label="Eigene Antworten erlauben:")


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
    description = forms.CharField(required=False, widget=forms.Textarea, label="Beschreibung:")
    password = forms.CharField(required=False, label="Passwort:")
    days = forms.IntegerField(required=False, min_value=0, max_value=65, label="Tage:")
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
    ))
    multiple_choice_allowed = forms.BooleanField(required=False, label="Mehrfachauswahl möglich:")


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
    description = forms.CharField(required=False, widget=forms.Textarea, label="Beschreibung:")
    password = forms.CharField(required=False, label="Passwort:")
    days = forms.IntegerField(required=False, min_value=0, max_value=65, label="Tage:")
    hours = forms.IntegerField(required=False, min_value=0, max_value=24, label="Stunden:")
    minutes = forms.IntegerField(required=False, min_value=0, max_value=60, label="Minuten:")
    # extra options
    show_result = forms.BooleanField(required=False, label="Ergebnis anzeigen:")
    logged_in_only = forms.BooleanField(required=False, label="Nur für angemeldete Nutzer:")
    # type-specific options
    num_tiers = forms.IntegerField(label="Tiers:", min_value=2, max_value=6, step_size=1, initial=6)


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
    description = forms.CharField(required=False, widget=forms.Textarea, label="Beschreibung:")
    password = forms.CharField(required=False, label="Passwort:")
    days = forms.IntegerField(required=False, min_value=0, max_value=65, label="Tage:")
    hours = forms.IntegerField(required=False, min_value=0, max_value=24, label="Stunden:")
    minutes = forms.IntegerField(required=False, min_value=0, max_value=60, label="Minuten:")
    # extra options
    show_result = forms.BooleanField(required=False, label="Ergebnis anzeigen:")
    logged_in_only = forms.BooleanField(required=False, label="Nur für angemeldete Nutzer:")
    # type-specific options
    criteria_good = forms.CharField(max_length=50, label="Kriterium: Gut", initial="gut")
    criteria_bad = forms.CharField(max_length=50, label="Kriterium: Schlecht", initial="schlecht")
