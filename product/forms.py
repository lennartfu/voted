from django import forms

from product.models import *


class ChoicePollForm(forms.ModelForm):
    class Meta:
        model = ChoicePoll
        fields = [
            "title",
            "description",
            "password",
            "timestamp_end",
            "show_result",
            "logged_in_only",
            "multiple_choice_allowed",
            "custom_answers_allowed",
        ]

    # basic fields
    title = forms.CharField(max_length=50, label="Titel:")
    description = forms.CharField(widget=forms.Textarea, label="Beschreibung:")
    password = forms.CharField(required=False, widget=forms.PasswordInput, label="Passwort:")
    timestamp_end = forms.DateTimeField(required=False, label="Enddatum:")
    # extra options
    show_result = forms.BooleanField(label="Ergebnis anzeigen:")
    logged_in_only = forms.BooleanField(label="Nur für angemeldete Nutzer:")
    # type-specific options
    multiple_choice_allowed = forms.BooleanField(label="Mehrfachauswahl möglich:")
    custom_answers_allowed = forms.BooleanField(label="Eigene Antworten erlauben:")


class DateTimePollForm(forms.ModelForm):
    class Meta:
        model = DateTimePoll
        fields = [
            "title",
            "description",
            "password",
            "timestamp_end",
            "show_result",
            "logged_in_only",
            "mode",
            "multiple_choice_allowed",
            "custom_answers_allowed",
        ]

    # basic fields
    title = forms.CharField(max_length=50, label="Titel:")
    description = forms.CharField(widget=forms.Textarea, label="Beschreibung:")
    password = forms.CharField(required=False, widget=forms.PasswordInput, label="Passwort:")
    timestamp_end = forms.DateTimeField(required=False, label="Enddatum:")
    # extra options
    show_result = forms.BooleanField(label="Ergebnis anzeigen:")
    logged_in_only = forms.BooleanField(label="Nur für angemeldete Nutzer:")
    # type-specific options
    mode = forms.ChoiceField(choices=(
        ("DAT", "Datum"),
        ("UHR", "Uhrzeit"),
        ("D&U", "Datum & Uhrzeit"),
    ))
    multiple_choice_allowed = forms.BooleanField(label="Mehrfachauswahl möglich:")
    custom_answers_allowed = forms.BooleanField(label="Eigene Antworten erlauben:")


class TierListPollForm(forms.ModelForm):
    class Meta:
        model = TierlistPoll
        fields = [
            "title",
            "description",
            "password",
            "timestamp_end",
            "show_result",
            "logged_in_only",
            "num_tiers",
        ]

    # basic fields
    title = forms.CharField(max_length=50, label="Titel:")
    description = forms.CharField(widget=forms.Textarea, label="Beschreibung:")
    password = forms.CharField(required=False, widget=forms.PasswordInput, label="Passwort:")
    timestamp_end = forms.DateTimeField(required=False, label="Enddatum:")
    # extra options
    show_result = forms.BooleanField(label="Ergebnis anzeigen:")
    logged_in_only = forms.BooleanField(label="Nur für angemeldete Nutzer:")
    # type-specific options
    num_tiers = forms.IntegerField(label="Tiers:", min_value=2, max_value=6, step_size=1)


class RankingPollForm(forms.ModelForm):
    class Meta:
        model = RankingPoll
        fields = [
            "title",
            "description",
            "password",
            "timestamp_end",
            "show_result",
            "logged_in_only",
            "criteria_good",
            "criteria_bad",
        ]

    # Basic fields
    title = forms.CharField(max_length=50, label="Titel:")
    description = forms.CharField(widget=forms.Textarea, label="Beschreibung:")
    password = forms.CharField(required=False, widget=forms.PasswordInput, label="Passwort:")
    timestamp_end = forms.DateTimeField(required=False, label="Enddatum:")
    # extra options
    show_result = forms.BooleanField(label="Ergebnis anzeigen:")
    logged_in_only = forms.BooleanField(label="Nur für angemeldete Nutzer:")
    # type-specific options
    criteria_good = forms.CharField(max_length=50, lable="Kriterium: Gut", initial="am besten")
    criteria_bad = forms.CharField(max_length=50, label="Kriterium: Schlecht", initial="am schlechtesten")
