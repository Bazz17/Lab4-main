import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from .models import Habit, UserHabit, ActivityLog, Goal, Badge, UserBadge, Tip
import random
from datetime import timedelta
from django.utils import timezone

# User Factory (za kreiranje korisnika)
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall('set_password', 'password123')


# Habit Factory
class HabitFactory(DjangoModelFactory):
    class Meta:
        model = Habit

    name = factory.Faker("word")
    description = factory.Faker("sentence", nb_words=10)
    points = factory.Faker('pyint', min_value=10, max_value=100)


# UserHabit Factory
class UserHabitFactory(DjangoModelFactory):
    class Meta:
        model = UserHabit

    user = factory.SubFactory(UserFactory)
    habit = factory.SubFactory(HabitFactory)
    frequency = factory.LazyAttribute(lambda _: random.choice(['daily', 'weekly', 'monthly']))
    start_date = factory.Faker('date_this_year', before_today=True)
    end_date = factory.LazyAttribute(lambda obj: obj.start_date + timedelta(days=random.randint(30, 180)))


# ActivityLog Factory
class ActivityLogFactory(DjangoModelFactory):
    class Meta:
        model = ActivityLog

    user_habit = factory.SubFactory(UserHabitFactory)
    date = factory.Faker('date_this_year', before_today=True)
    completed = factory.Faker('boolean')


# Goal Factory
class GoalFactory(DjangoModelFactory):
    class Meta:
        model = Goal

    user = factory.SubFactory(UserFactory)
    description = factory.Faker("sentence", nb_words=12)
    target_date = factory.Faker('future_date', end_date="+30d")
    achieved = factory.Faker('boolean')


# Badge Factory
class BadgeFactory(DjangoModelFactory):
    class Meta:
        model = Badge

    name = factory.Faker("word")
    description = factory.Faker("sentence", nb_words=10)
    icon = factory.django.ImageField(color="blue")
    criteria = factory.Faker("sentence", nb_words=6)


# UserBadge Factory
class UserBadgeFactory(DjangoModelFactory):
    class Meta:
        model = UserBadge

    user = factory.SubFactory(UserFactory)
    badge = factory.SubFactory(BadgeFactory)
    awarded_date = factory.Faker('date_this_year', before_today=True)


# Tip Factory
class TipFactory(DjangoModelFactory):
    class Meta:
        model = Tip

    title = factory.Faker("sentence", nb_words=6)
    content = factory.Faker("paragraph", nb_sentences=3)
    published_date = factory.LazyFunction(timezone.now)
