from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
 
class User(AbstractUser):

    GENDER = (
        ("M", "Male"),
        ("F", "Female"),
    )
    
    gender = models.CharField(max_length=30, blank=True, null=True, default="F", choices=GENDER)

    def __str__(self):
        return self.gender
