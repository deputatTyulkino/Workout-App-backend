from django.urls import path
from rest_framework import routers

from apps.exercise.views import CategoryAPIView, ExerciseViewSet

router = routers.SimpleRouter()
router.register(r'', ExerciseViewSet, basename='/')

urlpatterns = [
    path('categories/', CategoryAPIView.as_view()),
]

urlpatterns += router.urls
