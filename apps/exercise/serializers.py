from unicodedata import category

from rest_framework import serializers

from apps.accounts.serializers import AuthorExerciseSerializer, ProfileSerializer
from apps.exercise.models import Exercise, Category

VALID_ICON_NAME = ('core', 'legs', 'shoulders', 'arms', 'cardio')


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()

    class Meta:
        model = Category
        fields = '__all__'

    def validate_icon_name(self, value):
        if value not in VALID_ICON_NAME:
            raise serializers.ValidationError('Icon name is invalid')
        return value


class ExerciseSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    category = CategorySerializer()

    class Meta:
        model = Exercise
        fields = ('id', 'name', 'repeat', 'category')


class DetailExerciseSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    author = AuthorExerciseSerializer()

    class Meta:
        model = Exercise
        fields = '__all__'


class CreateExerciseSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Exercise
        fields = ('name', 'description', 'repeat', 'category')

    def create(self, validated_data):
        category_id = validated_data.pop('category_id')
        category = Category.objects.get(id=category_id)
        user = self.context['request'].user
        exercise = Exercise.objects.create(author=user, category=category, **validated_data)
        return exercise


class UpdateExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ('name', 'description', 'repeat', 'is_completed')


class DestroySerializer(serializers.Serializer):
    message = serializers.CharField(max_length=50)
