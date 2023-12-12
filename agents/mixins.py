from django.contrib.auth.mixins import AccessMixin
from django.urls import reverse


class AdminLoginRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_organisor or not request.user.is_authenticated:
            return reverse('leads:lead-list')
        return super().dispatch(request, *args, **kwargs)