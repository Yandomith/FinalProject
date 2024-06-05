from django.db import models
from django.contrib.auth.models import AbstractUser # type: ignore


# Create your models here.
class CustomUser(AbstractUser):
    pass
