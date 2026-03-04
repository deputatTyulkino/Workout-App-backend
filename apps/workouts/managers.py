from django.db import models


class WorkoutManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('author')

    def public_workouts(self):
        return self.get_queryset().filter(is_public=True)

    def not_public_workouts(self):
        return self.get_queryset().filter(is_public=False)
