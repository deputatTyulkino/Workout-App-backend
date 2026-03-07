from rest_framework import routers

from apps.workouts.views import WorkoutViewSet

router = routers.SimpleRouter()
router.register(r'', WorkoutViewSet, basename='/')
urlpatterns = router.urls
