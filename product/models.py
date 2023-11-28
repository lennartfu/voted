import uuid

from django.contrib.auth.models import User as DjangoUser
from django.db import models


def object_directory_path(instance, filename):
    return f"voted/objects/{instance.poll.code}/{filename}"


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.OneToOneField(DjangoUser, blank=True, null=True, on_delete=models.CASCADE)


# Poll models
class Poll(models.Model):
    created_date = models.DateTimeField(auto_now=True)
    code = models.CharField(max_length=5, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_created")
    participants = models.ManyToManyField(User, related_name="%(app_label)s_%(class)s_participated")
    members = models.ManyToManyField(User, related_name="%(app_label)s_%(class)s_invited")
    members_only = models.BooleanField(default=False)
    TYPE_CHOICES = (
        ("AB", "Abstimmung"),
        ("TR", "Termin"),
        ("TL", "Tierlist"),
        ("RA", "Rangliste"),
    )
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, editable=False)
    is_active = models.BooleanField(default=True)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    password = models.CharField(max_length=50, blank=True)
    ends_at = models.DateTimeField(blank=True, null=True)
    logged_in_only = models.BooleanField(default=False)
    show_result = models.BooleanField(default=False)

    class Meta:
        abstract = True


class ChoicePoll(Poll):
    multiple_choice_allowed = models.BooleanField(default=False)
    custom_answers_allowed = models.BooleanField(default=False)


class DateTimePoll(Poll):
    MODE_CHOICES = (
        ("DAT", "Datum"),
        ("UHR", "Uhrzeit"),
        ("D&U", "Datum & Uhrzeit"),
    )
    mode = models.CharField(max_length=3, choices=MODE_CHOICES, editable=False)
    multiple_choice_allowed = models.BooleanField(default=False)
    custom_answers_allowed = models.BooleanField(default=False)


class TierlistPoll(Poll):
    num_tiers = models.IntegerField()


class RankingPoll(Poll):
    criterium_best = models.CharField(max_length=50, default="am besten")
    criterium_worst = models.CharField(max_length=50, default="am schlechtesten")


# Object models
class ChoiceObject(models.Model):
    poll = models.ForeignKey(ChoicePoll, on_delete=models.CASCADE, related_name="objects")
    value = models.CharField(max_length=50)


class DateTimeObject(models.Model):
    poll = models.ForeignKey(DateTimePoll, on_delete=models.CASCADE, related_name="objects")
    value = models.DateTimeField()


class TierlistObject(models.Model):
    poll = models.ForeignKey(TierlistPoll, on_delete=models.CASCADE, related_name="objects")
    value = models.CharField(max_length=50)
    image = models.ImageField(upload_to=object_directory_path)


class RankingObject(models.Model):
    poll = models.ForeignKey(RankingPoll, on_delete=models.CASCADE, related_name="objects")
    value = models.CharField(max_length=50)


# Vote models
class ChoiceVote(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    poll = models.ForeignKey(ChoicePoll, on_delete=models.CASCADE, related_name="votes")
    data = models.JSONField()


class DateTimeVote(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    poll = models.ForeignKey(DateTimePoll, on_delete=models.CASCADE, related_name="votes")
    data = models.JSONField()


class TierlistVote(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    poll = models.ForeignKey(TierlistPoll, on_delete=models.CASCADE, related_name="votes")
    data = models.JSONField()


class RankingVote(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    poll = models.ForeignKey(RankingPoll, on_delete=models.CASCADE, related_name="votes")
    data = models.JSONField()
