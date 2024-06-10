from blog.views import ViewMetadataMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from .models import FeedbackForm


# Create your views here.
class FeedbackView(ViewMetadataMixin, TemplateView):
    template_name = "feedback/feedback.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = FeedbackForm()
        return context

    def post(self, request, *args, **kwargs):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("feedback:feedback")
        return self.get(request, *args, **kwargs)
