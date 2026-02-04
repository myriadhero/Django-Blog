from django.contrib.auth.mixins import AccessMixin
from django.http import Http404


class LoginRequired404Mixin(AccessMixin):
    """Require authentication and hide protected pages behind a 404."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404
        return super().dispatch(request, *args, **kwargs)
