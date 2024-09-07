from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from .forms import RegistrationForm


class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('shop:index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class LoginView(FormView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('shop:index')


class LogoutView(FormView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('users:login')
