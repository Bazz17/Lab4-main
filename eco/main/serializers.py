from rest_framework import serializers
from .models import *

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'name', 'description', 'points']  # Polja koja želimo izložiti putem API-ja

        def validate_points(self, value):
            if value <= 0:
             raise serializers.ValidationError("Bodovi trebaju biti veci od 0.")
            return value

class UserHabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserHabit
        fields = ['id','user_habit', 'date', 'completed']

        def validate(self, data):
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError("Datum pocetka ne moze biti iza datuma zavrsetka.")
            return data

class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = ['id', 'user', 'habit', 'frequency', 'start_date', 'end_date']

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'user', 'description', 'target_date', 'achieved']

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ['id', 'name', 'description', 'icon', 'criteria']

class UserBadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBadge
        fields = ['id','user', 'badge','awarded_date']

class TipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tip
        fields = ['id','title', 'content', 'published_date']