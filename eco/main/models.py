from django.db import models
from django.contrib.auth.models import User


class Habit(models.Model):
    """
    Represents an environmental habit that users can adopt.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    points = models.PositiveIntegerField(default=0)  # Points awarded for completing the habit

    def __str__(self):
        return self.name

class UserHabit(models.Model):
    """
    Links a user to a habit and tracks their commitment.
    """
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  # Optional end date

    def __str__(self):
        return f"{self.user.username} - {self.habit.name}"

class ActivityLog(models.Model):
    """
    Logs each time a user completes a habit.
    """
    user_habit = models.ForeignKey(UserHabit, on_delete=models.CASCADE)
    date = models.DateField()
    completed = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user_habit.user.username} - {self.date} - {'Completed' if self.completed else 'Missed'}"

class Goal(models.Model):
    """
    Allows users to set and track sustainability goals.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    target_date = models.DateField()
    achieved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.description}"

class Badge(models.Model):
    """
    Represents badges awarded to users for achievements.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField(upload_to='badges/')
    criteria = models.CharField(max_length=255)  # Criteria to earn the badge

    def __str__(self):
        return self.name

class UserBadge(models.Model):
    """
    Associates badges with users who have earned them.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    awarded_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"

class Tip(models.Model):
    """
    Provides sustainability tips to users.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
