import uuid

from django.contrib.auth import get_user_model
from django.db import models

from apps.exercise.managers import ExerciseManager

User = get_user_model()


# Create your models here.
class Category(models.Model):
    id = models.UUIDField(primary_key=True, editable=True, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=25, verbose_name='Name of category')
    description = models.TextField(verbose_name='Description of category')


class Exercise(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=50, verbose_name='Name of exercise')
    description = models.TextField(verbose_name='Description of exercise')
    icon = models.ImageField(verbose_name='Icon of exercise', upload_to='exercise_icon')
    repeat = models.IntegerField(verbose_name='Count of repeat', default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exercises')
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
