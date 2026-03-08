import uuid

from django.db import models
from django.conf import settings
from apps.exercise.managers import ExerciseManager


# Create your models here.
class Category(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=25, verbose_name='Name of category')
    description = models.TextField(verbose_name='Description of category')
    icon_name = models.CharField(verbose_name='Name of icon', max_length=10)


class Exercise(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=50, verbose_name='Name of exercise')
    description = models.TextField(verbose_name='Description of exercise')
    repeat = models.IntegerField(verbose_name='Count of repeat', default=0)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='exercises'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='exercises',
        verbose_name='Category of exercise'
    )
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ExerciseManager()

    class Meta:
        indexes = [models.Index(fields=('name', 'category'))]
