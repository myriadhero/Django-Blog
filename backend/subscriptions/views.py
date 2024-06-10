from django.forms import ModelForm
from django.shortcuts import render
from django.views.generic import UpdateView, View

from .models import Subscription


class SubscriptionForm(ModelForm):
    class Meta:
        model = Subscription
        fields = ("email",)


class SubscriptionCreateView(View):
    def post(self, request, *args, **kwargs):
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "subscriptions/success.html", {})
        return render(request, "subscriptions/email_form.html", {"email_sub_form": form})


class SubscriptionManageView(UpdateView):
    context_object_name = "subscription"
    model = Subscription
    fields = ("frequency",)

    def get(self, request, *args, **kwargs):
        if not (subscription := self.get_object()).confirmed:
            subscription.confirm()
        return super().get(request, *args, **kwargs)

    def get_template_names(self) -> list[str]:
        if self.request.headers.get("HX-Request"):
            return ["subscriptions/manage_form.html"]
        return ["subscriptions/manage.html"]
