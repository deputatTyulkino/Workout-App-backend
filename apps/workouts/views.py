from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response

from apps.workouts.models import Workout
from apps.workouts.serializers import WorkoutsSerializer, CreateWorkoutSerializer, DetailWorkoutSerializer, \
    DestroyWorkoutSerializer

tags = ['workouts']


# Create your views here.
class WorkoutViewSet(ModelViewSet):
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action == 'list':
            return WorkoutsSerializer
        elif self.action == 'create':
            return CreateWorkoutSerializer
        else:
            return DetailWorkoutSerializer

    def get_queryset(self):
        workouts = Workout.objects.filter(author=self.request.user)
        return workouts

    @extend_schema(
        summary='Получение списка тренировок',
        tags=tags
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary='Получение тренировки по id',
        tags=tags,
        parameters=[
            OpenApiParameter(
                name='workout_id',
                location='path',
                type=OpenApiTypes.UUID,
                description='ID тренировки'
            )
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary='Создание тренировки',
        tags=tags,
        request=CreateWorkoutSerializer,
        responses=DetailWorkoutSerializer
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary='Обновление тренировки',
        tags=tags,
        parameters=[
            OpenApiParameter(
                name='workout_id',
                description='ID тренировки',
                type=OpenApiTypes.UUID,
                location='path'
            )
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary='Удаление тренировки',
        tags=tags,
        responses={
            200: DestroyWorkoutSerializer
        },
        parameters=[
            OpenApiParameter(
                name='workout_id',
                description='ID тренировки',
                type=OpenApiTypes.UUID,
                location='path'
            )
        ]
    )
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return Response(
            data={'message': 'Delete is successfully'},
            status=status.HTTP_200_OK
        )
