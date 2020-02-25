from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView


class IndexTemplateView(LoginRequiredMixin, TemplateView):
    """
    Index view to load up vue front-end
    """

    def get_template_names(self):
        if settings.DEBUG is True:
            template_name = 'index_dev.html'
        else:
            template_name = 'index.html'
        return template_name
