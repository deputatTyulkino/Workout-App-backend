from rest_framework import serializers

from apps.accounts.serializers import AuthorExerciseSerializer, ProfileSerializer
from apps.exercise.models import Exercise, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ('id', 'name', 'description', 'icon', 'repeat')


class DetailExerciseSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    author = AuthorExerciseSerializer()

    class Meta:
        model = Exercise
        fields = '__all__'


class CreateExerciseSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    author = ProfileSerializer()

    class Meta:
        model = Exercise
        fields = ('name', 'description', 'icon', 'repeat', 'author', 'category')


class DestroySerializer(serializers.Serializer):
    message = serializers.CharField(max_length=50)
