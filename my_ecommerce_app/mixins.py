from django.core.exceptions import PermissionDenied
from users.models import User
from django.contrib.auth.models import AnonymousUser

class CustomerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return PermissionDenied
        elif request.user.is_customer:
            return super().dispatch(request, *args, **kwargs)
        else:
            return PermissionDenied


class VendorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return PermissionDenied
        elif request.user.is_vendor:
            return super().dispatch(request, *args, **kwargs)
        else:
            return PermissionDenied

class LoginNotAllowedMixin: # to prevent logged in users from accessing some views.
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return super().dispatch(request, *args, **kwargs) 
        else:
            return PermissionDenied

