from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


# Create your views here.


class EmailView(TemplateView):
    """Handle all the information on Email"""
    template_name = 'email/mailbox.html'
