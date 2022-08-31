from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Chef(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    restaurant = models.CharField(max_length=50, blank=True, null=True)


class Course(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    cover = models.FileField(upload_to='course_covers', blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    total_class = models.IntegerField(blank=True, null=True)
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='mentor')
    price = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)


class Enroll(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    txn_id = models.CharField(max_length=15, blank=True, null=True)
    banking = models.CharField(max_length=15, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='student')
    status = models.BooleanField(default=False, blank=True, null=True)
    enrolled_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


class Blog(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    cover = models.FileField(upload_to='blog_covers', blank=True, null=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
