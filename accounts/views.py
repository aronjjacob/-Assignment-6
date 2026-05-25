from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import RegisterForm, UserUpdateForm
from .models import UserProfile


class RegisterView(CreateView):
    """User registration view."""
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('album_list')
    
    def form_valid(self, form):
        user = form.save()
        # Create a user profile
        UserProfile.objects.get_or_create(user=user)
        # Log the user in after registration
        login(self.request, user)
        messages.success(self.request, f'Welcome, {user.username}! Your account has been created.')
        return redirect(self.success_url)


class ProfileView(LoginRequiredMixin, DetailView):
    """Display user profile."""
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'
    login_url = 'login'
    
    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = UserProfile.objects.get_or_create(user=self.request.user)[0]
        context['albums_count'] = self.request.user.albums.count()
        context['photos_count'] = self.request.user.photos.count()
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Update user profile."""
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('profile')
    login_url = 'login'
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been updated successfully!')
        return super().form_valid(form)
