from django.urls import path

from .views import SubscriptionCreateView, SubscriptionManageView

app_name = "subscriptions"

urlpatterns = [
    # Add your URL patterns here
    path("new/", SubscriptionCreateView.as_view(), name="new_sub"),
    path("<uuid:pk>/", SubscriptionManageView.as_view(), name="manage_sub"),
]
