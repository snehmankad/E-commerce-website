from django.core.exceptions import PermissionDenied
from users.models import User
from django.contrib.auth.models import AnonymousUser

def customer_permissions(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_anonymous:
            return PermissionDenied
        elif request.user.is_customer:
            return function(request, *args, **kwargs)
        else:
            return PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def vendor_permissions(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_anonymous:
            return PermissionDenied      
        elif request.user.is_vendor:
            return function(request, *args, **kwargs)
        else:
            return PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def login_not_allowed(function): # to prevent logged in users from accessing some views.
    def wrap(request, *args, **kwargs):
        if request.user.is_anonymous:
            return function(request, *args, **kwargs)
        else:
            return PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

