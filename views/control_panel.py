from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy

from jam.forms.profile import ProfileForm


class ControlPanelView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('login')
    template_name = "jam/control_panel.html"
    form_class = ProfileForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {
            'theme': self.request.user.profile.theme,
        }
        return kwargs

    def form_valid(self, form):
        profile = self.request.user.profile
        profile.theme = form.cleaned_data['theme']
        profile.save()
        return super().form_valid(form)
