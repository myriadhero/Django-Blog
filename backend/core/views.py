from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView

from .models import AboutPage, TermsPage


# Create your views here.
class AboutPageView(TemplateView):
    template_name = "core/about/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        about = AboutPage.objects.get_instance()
        context["about"] = about
        context["meta"] = about.as_meta(self.request)
        return context


class TermsPageView(TemplateView):
    template_name = "core/about/terms.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        terms = TermsPage.objects.get_instance()
        context["terms"] = terms
        context["meta"] = terms.as_meta(self.request)
        return context


def healthcheck_view(request):
    now = timezone.now()
    return HttpResponse(f"OK as of {now.isoformat()}")
