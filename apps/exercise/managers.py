from django.db import models


class ExerciseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('category').prefetch_related('workout')

    def completed_exercises(self):
        return self.filter(is_completed=True)

    def not_completed_exercises(self):
        return self.filter(is_completed=False)
