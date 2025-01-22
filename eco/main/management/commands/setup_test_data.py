import random

from django.db import transaction
from django.core.management.base import BaseCommand

from main.models import *
from main.factory import UserHabitFactory, HabitFactory, UserBadgeFactory, ActivityLogFactory, GoalFactory, TipFactory, BadgeFactory

NUM_HABIT = 30
NUM_USERHABIT = 30
NUM_ACTIVITYLOG = 15
NUM_GOAL = 15
NUM_BADGE = 15
NUM_USERBADGE = 30
NUM_TIP = 15

class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        models = [Habit, UserHabit, ActivityLog, Goal, Badge, UserBadge, Tip]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Creating new data...")

         # Generiranje podataka u batchu -- brzi nacin nego ovaj ispod sa for petljama
        HabitFactory.create_batch(NUM_HABIT)
        UserHabitFactory.create_batch(NUM_USERHABIT)
        ActivityLogFactory.create_batch(NUM_ACTIVITYLOG)
        GoalFactory.create_batch(NUM_GOAL)
        BadgeFactory.create_batch(NUM_BADGE)
        UserBadgeFactory.create_batch(NUM_USERBADGE)
        TipFactory.create_batch(NUM_TIP)

        self.stdout.write(self.style.SUCCESS("Test data successfully created!"))
       # for _ in range(NUM_HABIT):
        #    habit = HabitFactory()

        #for _ in range(NUM_USERHABIT):
         #   userhabit = UserHabitFactory()
        
        #for _ in range(NUM_ACTIVITYLOG):
         #   activity = ActivityLogFactory()

        #for _ in range(NUM_GOAL):
         #   goal = GoalFactory()

        #for _ in range(NUM_BADGE):
         #   badge = BadgeFactory()

        #for _ in range(NUM_USERBADGE):
         #   userbadge = UserBadgeFactory()

        #for _ in range(NUM_TIP):
         #   tip = TipFactory()