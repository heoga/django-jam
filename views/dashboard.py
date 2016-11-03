from django.views.generic.base import TemplateView


class DashboardView(TemplateView):

    template_name = "jam/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['test'] = 'Dashboard Test'
        return context
