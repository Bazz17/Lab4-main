from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView, LoginView, TemplateView
from django.urls import path, include
from . import views
#from .views import *
from .views import (
    HabitListView, HabitDetailView, HabitCreateView, HabitUpdateView, HabitDeleteView,
    UserHabitListView, UserHabitDetailView, UserHabitCreateView, UserHabitUpdateView, UserHabitDeleteView,
    ActivityLogListView, ActivityLogDetailView, ActivityLogCreateView, ActivityLogUpdateView, ActivityLogDeleteView,
    GoalListView, GoalDetailView, GoalCreateView, GoalUpdateView, GoalDeleteView,
    BadgeListView, BadgeDetailView, BadgeCreateView, BadgeUpdateView, BadgeDeleteView,
    UserBadgeListView, UserBadgeDetailView, UserBadgeCreateView, UserBadgeUpdateView, UserBadgeDeleteView,
    TipListView, TipDetailView, TipCreateView, TipUpdateView, TipDeleteView
)
from rest_framework.routers import DefaultRouter
from .views import HabitViewSet, UserHabitViewSet, ActivityLogViewSet, GoalViewSet, BadgeViewSet, UserBadgeViewSet, TipViewSet 
# da ne smaram i ubacujem u gornji dio, ljepse ovako

router = DefaultRouter()  # kreiranje jednog routera za sve modele

# registriranje svih modela za ruter
router.register(r'habits', HabitViewSet, basename='habit')  # /api/habits/
router.register(r'user-habits', UserHabitViewSet, basename='userhabit')  # /api/user-habits/
router.register(r'activity-logs', ActivityLogViewSet, basename='activitylog')  # /api/activity-logs/
router.register(r'goals', GoalViewSet, basename='goal')     # /api/goals/
router.register(r'badges', BadgeViewSet, basename='badge')  # /api/badges/
router.register(r'user-badges', UserBadgeViewSet, basename='userbadge')  # /api/user-badges/
router.register(r'tips', TipViewSet, basename='tip')   # /api/tips/


urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),  # Jedna ruta za login
    path('logout/', LogoutView.as_view(), name='logout'),  # Jedna ruta za logout
    path('logged-out/', TemplateView.as_view(template_name='logged_out.html'), name='logged_out'),  # Stranica nakon odjave
    path('register/', views.register, name='register'),  # Za registraciju
    path('', views.home_view, name='home'),  # Početna stranica
    path('home/', views.home_view, name='home'),  # Još jedna ruta za home
    
    path('api/', include(router.urls)),  # Dodavanje API ruta za prethodno registrirane modele iznad

    path('habits/', HabitListView.as_view(), name='habit_list'),
    path('goals/', GoalListView.as_view(), name='goal_list'),
    path('tips/', TipListView.as_view(), name='tip_list'),
    path('badges/', BadgeListView.as_view(), name='badge_list'),
    path('activity-log/', ActivityLogListView.as_view(), name='activity_log_list'),


    # Habit
    path('habits/', HabitListView.as_view(), name='habit-list'),
    path('habits/<int:pk>/', HabitDetailView.as_view(), name='habit-detail'),
    path('habits/create/', HabitCreateView.as_view(), name='habit-create'),
    path('habits/<int:pk>/update/', HabitUpdateView.as_view(), name='habit-update'),
    path('habits/<int:pk>/delete/', HabitDeleteView.as_view(), name='habit-delete'),
    
    # UserHabit
    path('user-habits/', UserHabitListView.as_view(), name='userhabit-list'),
    path('user-habits/<int:pk>/', UserHabitDetailView.as_view(), name='userhabit-detail'),
    path('user_habits/create/', UserHabitCreateView.as_view(), name='user_habit-create'),
    path('user_habits/<int:pk>/update/', UserHabitUpdateView.as_view(), name='user_habit-update'),
    path('user_habits/<int:pk>/delete/', UserHabitDeleteView.as_view(), name='user_habit-delete'),
    
    # ActivityLog
    path('activity-logs/', ActivityLogListView.as_view(), name='activitylog-list'),
    path('activity-logs/<int:pk>/', ActivityLogDetailView.as_view(), name='activitylog-detail'),
     path('activity_logs/create/', ActivityLogCreateView.as_view(), name='activity_log-create'),
    path('activity_logs/<int:pk>/update/', ActivityLogUpdateView.as_view(), name='activity_log-update'),
    path('activity_logs/<int:pk>/delete/', ActivityLogDeleteView.as_view(), name='activity_log-delete'),

    
    # Goal
    path('goals/', GoalListView.as_view(), name='goal-list'),
    path('goals/<int:pk>/', GoalDetailView.as_view(), name='goal-detail'),
    path('goals/create/', GoalCreateView.as_view(), name='goal-create'),
    path('goals/<int:pk>/update/', GoalUpdateView.as_view(), name='goal-update'),
    path('goals/<int:pk>/delete/', GoalDeleteView.as_view(), name='goal-delete'),
    
    # Badge
    path('badges/', BadgeListView.as_view(), name='badge-list'),
    path('badges/<int:pk>/', BadgeDetailView.as_view(), name='badge-detail'),
    path('badges/create/', BadgeCreateView.as_view(), name='badge-create'),
    path('badges/<int:pk>/update/', BadgeUpdateView.as_view(), name='badge-update'),
    path('badges/<int:pk>/delete/', BadgeDeleteView.as_view(), name='badge-delete'),
    
    # UserBadge
    path('user-badges/', UserBadgeListView.as_view(), name='userbadge-list'),
    path('user-badges/<int:pk>/', UserBadgeDetailView.as_view(), name='userbadge-detail'),
    path('user_badges/create/', UserBadgeCreateView.as_view(), name='user_badge-create'),
    path('user_badges/<int:pk>/update/', UserBadgeUpdateView.as_view(), name='user_badge-update'),
    path('user_badges/<int:pk>/delete/', UserBadgeDeleteView.as_view(), name='user_badge-delete'),
    
    # Tip
    path('tips/', TipListView.as_view(), name='tip-list'),
    path('tips/<int:pk>/', TipDetailView.as_view(), name='tip-detail'),
    path('tips/create/', TipCreateView.as_view(), name='tip-create'),
    path('tips/<int:pk>/update/', TipUpdateView.as_view(), name='tip-update'),
    path('tips/<int:pk>/delete/', TipDeleteView.as_view(), name='tip-delete'),
]