from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
import uuid

from apps.accounts.managers import UserManager


# Create your models here.
class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    email = models.EmailField(unique=True, verbose_name='Email')
    username = models.CharField(max_length=255, verbose_name='Username', null=True)
    image_before = models.ImageField(
        upload_to='profile_image',
        null=True,
        verbose_name='Before User image'
    )
    image_after = models.ImageField(
        upload_to='profile_image',
        null=True,
        verbose_name='After User image'
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date of create')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Date of update')

    workout_minutes = models.IntegerField(verbose_name='All time workouts', default=0)
    workouts_count = models.IntegerField(verbose_name='Workouts count', default=0)
    weight_lifted = models.IntegerField(verbose_name='Weight lifted', default=0)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    @property
    def is_superuser(self):
        return self.is_staff

    def __str__(self):
        return self.username if self.username else self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
