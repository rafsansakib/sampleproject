from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=10, null=True, blank=True, default="student")
    cover = models.FileField(upload_to='profile_photos', blank=True, null=True)
