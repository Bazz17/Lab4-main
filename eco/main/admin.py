from django.contrib import admin
from .models import *
from django.contrib.auth.models import User


model_list = [Habit, UserHabit, ActivityLog, Goal, Badge, UserBadge, Tip]
admin.site.register(model_list)

