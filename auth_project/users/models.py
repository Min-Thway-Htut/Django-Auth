from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class CustomUser(AbstractUser):
    is_approved = models.BooleanField(default=False)
    registration_code = models.UUIDField(default=uuid.uuid4, editable=False)
    

    