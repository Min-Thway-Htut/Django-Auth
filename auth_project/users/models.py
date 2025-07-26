from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class CustomUser(AbstractUser):
    is_approved = models.BooleanField(default=False)
    approval_token = models.UUIDField(default=uuid.uuid4, unique=True, null=True, blank=True)
    