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
    category_id = serializers.UUIDField()

    class Meta:
        model = Exercise
        fields = ('name', 'description', 'repeat', 'category_id')

    def create(self, validated_data):
        category_id = validated_data.pop('category_id')
        try:
            exercise_category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise serializers.ValidationError('Not Found category with this ID')
        user = self.context['request'].user
        exercise = Exercise.objects.create(
            author=user, category=exercise_category, **validated_data
        )
        return exercise


class UpdateExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ('name', 'description', 'repeat', 'is_completed')


class DestroySerializer(serializers.Serializer):
    message = serializers.CharField(max_length=50)
