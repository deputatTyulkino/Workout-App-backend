from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from apps.accounts.serializers import AuthorExerciseSerializer
from apps.exercise.models import Exercise
from apps.exercise.serializers import ExerciseSerializer
from apps.workouts.models import Workout


class WorkoutsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ('id', 'name', 'is_completed')


class CreateWorkoutSerializer(serializers.ModelSerializer):
    exercises = PrimaryKeyRelatedField(
        many=True, queryset=Exercise.objects.all()
    )

    class Meta:
        model = Workout
        fields = ('name', 'description', 'duration', 'exercises')

    def create(self, validated_data):
        user = self.context['request'].user
        exercises = validated_data.pop('exercises')
        workout = Workout.objects.create(author=user, **validated_data)
        workout.exercises.add(exercises)
        return workout


class DetailWorkoutSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True)
    author = AuthorExerciseSerializer()

    class Meta:
        model = Workout
        fields = '__all__'


class UpdateWorkoutSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True)

    class Meta:
        model = Workout
        fields = ('name', 'description', 'duration', 'is_completed', 'is_public', 'exercises')


class DestroyWorkoutSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=50)
