from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import authenticate, login
from django.db.models import Q
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import *


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')

    else:
        form = UserCreationForm()

    context = {'form': form}

    return render(request, 'registration/register.html', context)


# Provjera da li je korisnik administrator
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Administrator').exists())
def admin_view(request):
    return render(request, 'admin_dashboard.html')
# za običnog smrtnika -> korisnika
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Korisnik').exists())
def user_view(request):
    return render(request, 'user_dashboard.html')

def home_view(request):
    return render(request, 'home.html')


# Base ListView s pretraživanjem
class BaseSearchListView(ListView):
    search_fields = []  # Polja po kojima se pretražuje
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = super().get_queryset()
        if query and self.search_fields:
            q_objects = Q()
            for field in self.search_fields:
                q_objects |= Q(**{f"{field}__icontains": query})
            return queryset.filter(q_objects)
        return queryset

# Habit
class HabitListView(BaseSearchListView):
    model = Habit
    template_name = 'habits/habit_list.html'
    context_object_name = 'habits'
    search_fields = ['name', 'description']

class HabitDetailView(DetailView):
    model = Habit
    template_name = 'habits/habit_detail.html'
    context_object_name = 'habit'

class HabitViewSet(viewsets.ModelViewSet):   # ViewSet - klasa iz Django Rest Frameworka za automatsko rukovanje CRUD operacijama
    """
    API endpoint za upravljanje Habit modelom.
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]  # Ograničavanje pristupa samo za prijavljene korisnike, u nastavku za svaki model

# UserHabit
class UserHabitListView(BaseSearchListView):
    model = UserHabit
    template_name = 'user_habits/user_habit_list.html'
    context_object_name = 'user_habits'
    search_fields = ['user__username', 'habit__name', 'frequency']

class UserHabitDetailView(DetailView):
    model = UserHabit
    template_name = 'user_habits/user_habit_detail.html'
    context_object_name = 'user_habit'

class UserHabitViewSet(viewsets.ModelViewSet):
    """
    API endpoint za upravljanje UserHabit modelom.
    """
    queryset = UserHabit.objects.all()
    serializer_class = UserHabitSerializer
    permission_classes = [IsAuthenticated] 

# ActivityLog
class ActivityLogListView(BaseSearchListView):
    model = ActivityLog
    template_name = 'activity_logs/activity_log_list.html'
    context_object_name = 'activity_logs'
    search_fields = ['user_habit__user__username', 'date']

class ActivityLogDetailView(DetailView):
    model = ActivityLog
    template_name = 'activity_logs/activity_log_detail.html'
    context_object_name = 'activity_log'

class ActivityLogViewSet(viewsets.ModelViewSet):
    """
    API endpoint za upravljanje ActivityLog modelom.
    """
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAuthenticated] 

# Goal
class GoalListView(BaseSearchListView):
    model = Goal
    template_name = 'goals/goal_list.html'
    context_object_name = 'goals'
    search_fields = ['user__username', 'description']

class GoalDetailView(DetailView):
    model = Goal
    template_name = 'goals/goal_detail.html'
    context_object_name = 'goal'

class GoalViewSet(viewsets.ModelViewSet):
    """
    API endpoint za upravljanje Goal modelom.
    """
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated] 

# Badge
class BadgeListView(BaseSearchListView):
    model = Badge
    template_name = 'badges/badge_list.html'
    context_object_name = 'badges'
    search_fields = ['name', 'description', 'criteria']

class BadgeDetailView(DetailView):
    model = Badge
    template_name = 'badges/badge_detail.html'
    context_object_name = 'badge'

class BadgeViewSet(viewsets.ModelViewSet):
    """
    API endpoint za upravljanje Badge modelom.
    """
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = [IsAuthenticated] 

# UserBadge
class UserBadgeListView(BaseSearchListView):
    model = UserBadge
    template_name = 'user_badges/user_badge_list.html'
    context_object_name = 'user_badges'
    search_fields = ['user__username', 'badge__name']

class UserBadgeDetailView(DetailView):
    model = UserBadge
    template_name = 'user_badges/user_badge_detail.html'
    context_object_name = 'user_badge'

class UserBadgeViewSet(viewsets.ModelViewSet):
    """
    API endpoint za upravljanje UserBadge modelom.
    """
    queryset = UserBadge.objects.all()
    serializer_class = UserBadgeSerializer
    permission_classes = [IsAuthenticated] 

# Tip
class TipListView(BaseSearchListView):
    model = Tip
    template_name = 'tips/tip_list.html'
    context_object_name = 'tips'
    search_fields = ['title', 'content']

class TipDetailView(DetailView):
    model = Tip
    template_name = 'tips/tip_detail.html'
    context_object_name = 'tip'

class TipViewSet(viewsets.ModelViewSet):
    """
    API endpoint za upravljanje Tip modelom.
    """
    queryset = Tip.objects.all()
    serializer_class = TipSerializer
    permission_classes = [IsAuthenticated] 

##############################################################################
# Habit CRUD
class HabitCreateView(LoginRequiredMixin, CreateView):
    model = Habit
    template_name = 'habits/habit_form.html'
    fields = ['name', 'description', 'points']

    def form_valid(self, form):
        return super().form_valid(form)

class HabitUpdateView(LoginRequiredMixin, UpdateView):
    model = Habit
    template_name = 'habits/habit_form.html'
    fields = ['name', 'description', 'points']

    def form_valid(self, form):
        return super().form_valid(form)

class HabitDeleteView(LoginRequiredMixin, DeleteView):
    model = Habit
    template_name = 'habits/habit_confirm_delete.html'
    success_url = reverse_lazy('habit-list')

# UserHabit CRUD
class UserHabitCreateView(LoginRequiredMixin, CreateView):
    model = UserHabit
    template_name = 'user_habits/user_habit_form.html'
    fields = ['user', 'habit', 'frequency', 'start_date', 'end_date']

    def form_valid(self, form):
        return super().form_valid(form)

class UserHabitUpdateView(LoginRequiredMixin, UpdateView):
    model = UserHabit
    template_name = 'user_habits/user_habit_form.html'
    fields = ['user', 'habit', 'frequency', 'start_date', 'end_date']

    def form_valid(self, form):
        return super().form_valid(form)

class UserHabitDeleteView(LoginRequiredMixin, DeleteView):
    model = UserHabit
    template_name = 'user_habits/user_habit_confirm_delete.html'
    success_url = reverse_lazy('user_habit-list')

# ActivityLog CRUD
class ActivityLogCreateView(LoginRequiredMixin, CreateView):
    model = ActivityLog
    template_name = 'activity_logs/activity_log_form.html'
    fields = ['user_habit', 'date', 'completed']

    def form_valid(self, form):
        return super().form_valid(form)

class ActivityLogUpdateView(LoginRequiredMixin, UpdateView):
    model = ActivityLog
    template_name = 'activity_logs/activity_log_form.html'
    fields = ['user_habit', 'date', 'completed']

    def form_valid(self, form):
        return super().form_valid(form)

class ActivityLogDeleteView(LoginRequiredMixin, DeleteView):
    model = ActivityLog
    template_name = 'activity_logs/activity_log_confirm_delete.html'
    success_url = reverse_lazy('activity_log-list')

# Goal CRUD
class GoalCreateView(LoginRequiredMixin, CreateView):
    model = Goal
    template_name = 'goals/goal_form.html'
    fields = ['user', 'description', 'target_date', 'achieved']

    def form_valid(self, form):
        return super().form_valid(form)

class GoalUpdateView(LoginRequiredMixin, UpdateView):
    model = Goal
    template_name = 'goals/goal_form.html'
    fields = ['user', 'description', 'target_date', 'achieved']

    def form_valid(self, form):
        return super().form_valid(form)

class GoalDeleteView(LoginRequiredMixin, DeleteView):
    model = Goal
    template_name = 'goals/goal_confirm_delete.html'
    success_url = reverse_lazy('goal-list')

# Badge CRUD
class BadgeCreateView(LoginRequiredMixin, CreateView):
    model = Badge
    template_name = 'badges/badge_form.html'
    fields = ['name', 'description', 'icon', 'criteria']

    def form_valid(self, form):
        return super().form_valid(form)

class BadgeUpdateView(LoginRequiredMixin, UpdateView):
    model = Badge
    template_name = 'badges/badge_form.html'
    fields = ['name', 'description', 'icon', 'criteria']

    def form_valid(self, form):
        return super().form_valid(form)

class BadgeDeleteView(LoginRequiredMixin, DeleteView):
    model = Badge
    template_name = 'badges/badge_confirm_delete.html'
    success_url = reverse_lazy('badge-list')

# UserBadge CRUD
class UserBadgeCreateView(LoginRequiredMixin, CreateView):
    model = UserBadge
    template_name = 'user_badges/user_badge_form.html'
    fields = ['user', 'badge', 'awarded_date']

    def form_valid(self, form):
        return super().form_valid(form)

class UserBadgeUpdateView(LoginRequiredMixin, UpdateView):
    model = UserBadge
    template_name = 'user_badges/user_badge_form.html'
    fields = ['user', 'badge', 'awarded_date']

    def form_valid(self, form):
        return super().form_valid(form)

class UserBadgeDeleteView(LoginRequiredMixin, DeleteView):
    model = UserBadge
    template_name = 'user_badges/user_badge_confirm_delete.html'
    success_url = reverse_lazy('user_badge-list')

# Tip CRUD
class TipCreateView(LoginRequiredMixin, CreateView):
    model = Tip
    template_name = 'tips/tip_form.html'
    fields = ['title', 'content', 'published_date']

    def form_valid(self, form):
        return super().form_valid(form)

class TipUpdateView(LoginRequiredMixin, UpdateView):
    model = Tip
    template_name = 'tips/tip_form.html'
    fields = ['title', 'content', 'published_date']

    def form_valid(self, form):
        return super().form_valid(form)

class TipDeleteView(LoginRequiredMixin, DeleteView):
    model = Tip
    template_name = 'tips/tip_confirm_delete.html'
    success_url = reverse_lazy('tip-list')
