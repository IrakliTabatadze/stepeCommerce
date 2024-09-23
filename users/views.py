from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RegistrationForm, ProfileForm
from .models import Profile


class RegistrationUserView(FormView):
    form_class = RegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('shop:index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        profile = Profile.objects.create(user=user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class LoginUserView(LoginView):
    template_name = 'users/login.html'


class LogoutUserView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('users:login')

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('users:login')


class ProfileView(LoginRequiredMixin, View):
    login_url = reverse_lazy('users:login')

    def get(self, request):
        # Get user profile and user info
        profile, _ = Profile.objects.get_or_create(user=request.user)
        profile_form = ProfileForm(instance=profile)
        password_form = PasswordChangeForm(user=request.user)

        context = {
            'profile': profile,
            'profile_form': profile_form,
            'password_form': password_form,
            'user': request.user,  # Include user for additional user information
        }
        return render(request, 'users/profile.html', context)

    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        # Handle password change
        password_form = PasswordChangeForm(user=request.user, data=request.POST)

        if 'update_profile' in request.POST:  # Profile update form is submitted
            if profile_form.is_valid():
                profile_form.save()
                return redirect('users:profile')

        elif 'change_password' in request.POST:  # Password change form is submitted
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Keeps user logged in after password change
                return redirect('users:profile')

        context = {
            'profile_form': profile_form,
            'password_form': password_form,
            'user': request.user,
        }
        return render(request, 'users/profile.html', context)