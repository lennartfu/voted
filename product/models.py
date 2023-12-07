import uuid

import shortuuid
from django.contrib.auth.models import User as DjangoUser
from django.db import models


def generate_unique_code():
    # generate a 5 digit code
    shortuuid.set_alphabet("0123456789")
    code = shortuuid.uuid()[:5]
    # make sure the code doesn't exist yet
    while (ChoicePoll.objects.filter(code=code).exists() or
           DateTimePoll.objects.filter(code=code).exists() or
           TierlistPoll.objects.filter(code=code).exists() or
           RankingPoll.objects.filter(code=code).exists()):
        code = shortuuid.uuid()[:5]
    return code


def object_directory_path(instance, filename):
    return f"product/media/objects/{instance.poll.code}/{filename}"


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.OneToOneField(DjangoUser, blank=True, null=True, on_delete=models.CASCADE)


# Poll base model
class Poll(models.Model):
    class Meta:
        abstract = True

    # basic attributes
    is_active = models.BooleanField(default=True)
    code = models.CharField(max_length=5, default=generate_unique_code, editable=False)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    password = models.CharField(max_length=50, blank=True)
    # timestamps
    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_end = models.DateTimeField(blank=True, null=True)
    # associated users
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)ss_created"  # reverse example: user.product_choicepolls_created
    )
    participants = models.ManyToManyField(
        User,
        blank=True,
        related_name="%(app_label)s_%(class)ss_participated"  # reverse example: user.product_choicepolls_participated
    )
    # extra options
    show_result = models.BooleanField(default=False)
    logged_in_only = models.BooleanField(default=False)


# Poll models
class ChoicePoll(Poll):
    multiple_choice_allowed = models.BooleanField(default=False)
    custom_answers_allowed = models.BooleanField(default=False)


class DateTimePoll(Poll):
    MODE_CHOICES = (
        ("DAT", "Datum"),
        ("UHR", "Uhrzeit"),
        ("D&U", "Datum & Uhrzeit"),
    )
    mode = models.CharField(max_length=3, choices=MODE_CHOICES)
    multiple_choice_allowed = models.BooleanField(default=False)
    custom_answers_allowed = models.BooleanField(default=False)


class TierlistPoll(Poll):
    num_tiers = models.PositiveSmallIntegerField()


class RankingPoll(Poll):
    criteria_good = models.CharField(max_length=50, default="gut")
    criteria_bad = models.CharField(max_length=50, default="schlecht")


# Object models
class ChoiceObject(models.Model):
    poll = models.ForeignKey(ChoicePoll, on_delete=models.CASCADE, related_name="vote_objects")
    value = models.CharField(max_length=50)


class DateTimeObject(models.Model):
    poll = models.ForeignKey(DateTimePoll, on_delete=models.CASCADE, related_name="vote_objects")
    value = models.DateTimeField()


class TierlistObject(models.Model):
    poll = models.ForeignKey(TierlistPoll, on_delete=models.CASCADE, related_name="vote_objects")
    value = models.CharField(max_length=50)
    image = models.ImageField(upload_to=object_directory_path)


class RankingObject(models.Model):
    poll = models.ForeignKey(RankingPoll, on_delete=models.CASCADE, related_name="vote_objects")
    value = models.CharField(max_length=50)
    image = models.ImageField(upload_to=object_directory_path)


# Vote base model
class VoteModel(models.Model):
    class Meta:
        abstract = True

    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)ss")  # reverse example: user.product_choicevotes
    data = models.JSONField()
    last_updated = models.DateTimeField(auto_now=True)


# Vote models
class ChoiceVote(VoteModel):
    poll = models.ForeignKey(ChoicePoll, on_delete=models.CASCADE, related_name="votes")


class DateTimeVote(VoteModel):
    poll = models.ForeignKey(DateTimePoll, on_delete=models.CASCADE, related_name="votes")


class TierlistVote(VoteModel):
    poll = models.ForeignKey(TierlistPoll, on_delete=models.CASCADE, related_name="votes")


class RankingVote(VoteModel):
    poll = models.ForeignKey(RankingPoll, on_delete=models.CASCADE, related_name="votes")
