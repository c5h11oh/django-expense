from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='my_account')
    dob = models.DateField(verbose_name='Date of Birth', blank=True)