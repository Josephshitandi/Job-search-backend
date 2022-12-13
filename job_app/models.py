from django.db import models
import cloudinary
from cloudinary.models import CloudinaryField
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _

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


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        print("email...", email)
        print("password...", password)
        return self._create_user(email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    CUSTOMER = 1
    MERCHANT = 2
    ADMIN = 3
    ROLE_CHOICES = (
        (CUSTOMER, 'customer'),
        (MERCHANT, 'merchant'),
        (ADMIN, 'admin'),
    )
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(default=False)
    user_type = models.IntegerField(choices=ROLE_CHOICES, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Profile(models.Model):
    username = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='profile')
    avatar = CloudinaryField('avatar', null=True, blank=True)
    address = models.CharField(max_length=30)
    phone_number = models.IntegerField()
    region = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.user.last_name} Profile'

    def save_profile(self):
        self.save

    def delete_profile(self):
        self.delete()
