import uuid

from django.db import models
from django.conf import settings
from apps.exercise.models import Exercise
from apps.workouts.managers import WorkoutManager


# Create your models here.
class Workout(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=50, verbose_name='Name of workout')
    description = models.TextField(verbose_name='Description of workout')
    duration = models.IntegerField(verbose_name='Duration of workout (minutes)')
    exercises = models.ManyToManyField(
        Exercise, verbose_name='Exercises', related_name='workouts'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='workouts',
        verbose_name='Author of workout'
    )
    is_completed = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = WorkoutManager()

    class Meta:
        indexes = [models.Index(fields=('name', 'author'))]
