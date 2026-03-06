from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from apps.exercise.models import Exercise, Category
from apps.exercise.serializers import (
    ExerciseSerializer, CategorySerializer, DetailExerciseSerializer, CreateExerciseSerializer, DestroySerializer
)
from rest_framework import status

tags = ['exercise']


# Create your views here.
class CategoryAPIView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    @extend_schema(
        summary='Получение категорий упражнений',
        tags=tags
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ExerciseAPIView(ModelViewSet):
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action == 'list':
            return ExerciseSerializer
        elif self.action == 'create':
            return CreateExerciseSerializer
        else:
            return DetailExerciseSerializer

    def get_queryset(self):
        exercises = (Exercise.objects
                     .not_completed_exercises()
                     .filter(author=self.request.user))
        return exercises

    @extend_schema(
        summary='Получение списка упражнений',
        tags=tags,
        responses=ExerciseSerializer
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary='Получение определённого упражнения',
        tags=tags,
        responses=DetailExerciseSerializer,
        parameters=[OpenApiParameter(
            name='exercise_id',
            type=OpenApiTypes.UUID,
            location='path',
            description='ID упражнения для его получения'
        )]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary='Создание упражнения',
        tags=tags,
        request=CreateExerciseSerializer,
        responses=ExerciseSerializer
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary='Обновление данных упражнения',
        tags=tags,
        responses=DetailExerciseSerializer,
        parameters=[
            OpenApiParameter(
                name='exercise_id',
                type=OpenApiTypes.UUID,
                location='path',
                description='ID упражнения для его удаления'
            )
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary='Удаление упражнения',
        tags=tags,
        responses={
            200: DestroySerializer
        },
        parameters=[
            OpenApiParameter(
                name='exercise_id',
                type=OpenApiTypes.UUID,
                location='path',
                description='ID упражнения для его удаления'
            )
        ]
    )
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return Response(
            data={'message': 'Delete is successfully'},
            status=status.HTTP_200_OK
        )
