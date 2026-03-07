from unicodedata import category

from rest_framework import serializers

from apps.accounts.serializers import AuthorExerciseSerializer, ProfileSerializer
from apps.exercise.models import Exercise, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ExerciseSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()

    class Meta:
        model = Exercise
        fields = ('id', 'name', 'icon', 'repeat')


class DetailExerciseSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    author = AuthorExerciseSerializer()

    class Meta:
        model = Exercise
        fields = '__all__'


class CreateExerciseSerializer(serializers.ModelSerializer):
    category_id = serializers.UUIDField()

    class Meta:
        model = Exercise
        fields = ('name', 'description', 'icon', 'repeat', 'category_id')

    def create(self, validated_data):
        category_id = validated_data.pop('category_id')
        category = Category.objects.get(id=category_id)
        user = self.context['request'].user
        exercise = Exercise.objects.create(author=user, category=category, **validated_data)
        return exercise


class DestroySerializer(serializers.Serializer):
    message = serializers.CharField(max_length=50)
