from django.contrib import admin

from .models import *

admin.site.register([User, ChoicePoll, DateTimePoll, TierlistPoll, RankingPoll])
