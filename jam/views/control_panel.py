from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy

from django.shortcuts import render
from django.views import View

from jam.forms.profile import ProfileForm
from jam.forms.user import UserForm


class OldControlPanelView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = "jam/control_panel.html"
    form_class = ProfileForm
    second_form_class = UserForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {
            'theme': self.request.user.profile.theme,
            'first_name': self.request.user.first_name,
            'email': self.request.user.email,
        }
        return kwargs

    def form_valid(self, form):
        profile = self.request.user.profile
        profile.theme = form.cleaned_data['theme']
        profile.save()
        return super().form_valid(form)


class ControlPanelView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    template_name = "jam/control_panel.html"

    def get(self, request, *args, **kwargs):
        user_form = UserForm(initial={
            'first_name': self.request.user.first_name,
            'last_name': self.request.user.last_name,
            'email': self.request.user.email,
        })
        profile_form = ProfileForm(initial={
            'theme': self.request.user.profile.theme
        })
        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form,
        })

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            # <process form cleaned data>
            for key, value in user_form.cleaned_data.items():
                setattr(self.request.user, key, value)
            for key, value in profile_form.cleaned_data.items():
                setattr(self.request.user.profile, key, value)
            self.request.user.save()
            self.request.user.profile.save()
        return self.get(request, *args, **kwargs)
