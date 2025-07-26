from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import PermissionDenied

class ApprovalBackend(ModelBackend):
    def authenticate(self, request, username = ..., password = ..., **kwargs):
        user = super().authenticate(request, username, password, **kwargs)
        if user and not user.is_approved:
            raise PermissionDenied("Your account is awaiting approval.")
        return user