from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

# from .managers import UserManager
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.
class Job(models.Model):
    job_title = models.CharField(max_length=100)
    description = models.TextField()
    date_published = models.DateTimeField(auto_now_add=True)
    company = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=100)

    def __str__(self):
        return self.sjob_title

    def save_job(self):
        self.save()

    def delete_delete(self):
        self.delete()
