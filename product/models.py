import uuid

import shortuuid
from django.contrib.auth.models import User as DjangoUser
from django.db import models

from voted.settings import MEDIA_ROOT


def generate_unique_code():
    # generate a 5 digit code
    shortuuid.set_alphabet("0123456789")
    code = shortuuid.uuid()[:5]
    # make sure the code doesn't exist yet
    while Poll.objects.filter(code=code).exists():
        code = shortuuid.uuid()[:5]
    return code


def option_directory_path(instance, filename):
    return f"voting_options/{instance.poll.code}/{filename}"


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.OneToOneField(DjangoUser, blank=True, null=True, on_delete=models.CASCADE)


class Poll(models.Model):
    # poll type
    TYPE_CHOICES = (
        ("POLL", "Umfrage"),
        ("DATE", "Terminabstimmung"),
        ("TIER", "Tierlist"),
        ("RANK", "Rangliste"),
    )
    poll_type = models.CharField(max_length=4, choices=TYPE_CHOICES)
    # basic attributes
    is_active = models.BooleanField(default=True)
    code = models.CharField(max_length=5, default=generate_unique_code, editable=False)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500, blank=True)
    password = models.CharField(max_length=50, blank=True)
    # timestamps
    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_end = models.DateTimeField(blank=True, null=True)
    timestamp_changed = models.DateTimeField(auto_now=True)
    # associated users
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="polls_created",
    )
    participants = models.ManyToManyField(
        User,
        blank=True,
        related_name="polls_participated",
    )
    viewers = models.ManyToManyField(
        User,
        blank=True,
        related_name="polls_viewed",
        through="PollView",
    )
    # extra options
    show_result = models.BooleanField(default=False)
    logged_in_only = models.BooleanField(default=False)
    multiple_choice_allowed = models.BooleanField(default=False)
    custom_answers_allowed = models.BooleanField(default=False)
    # date poll options
    DATE_MODE_CHOICES = (
        ("DATE", "Datum"),
        ("TIME", "Uhrzeit"),
        ("BOTH", "Datum & Uhrzeit"),
    )
    date_mode = models.CharField(blank=True, null=True, max_length=4, choices=DATE_MODE_CHOICES)
    # tierlist poll options
    num_tiers = models.PositiveSmallIntegerField(blank=True, null=True)
    # ranking poll options
    criteria_good = models.CharField(blank=True, null=True, max_length=50)
    criteria_bad = models.CharField(blank=True, null=True, max_length=50)


class PollView(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)


class VotingOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="voting_options")
    text = models.CharField(blank=True, null=True, max_length=50)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to=option_directory_path)


class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="votes")
    data = models.JSONField()
    last_updated = models.DateTimeField(auto_now=True)
