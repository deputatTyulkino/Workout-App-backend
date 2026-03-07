from rest_framework import serializers

from apps.accounts.serializers import AuthorExerciseSerializer
from apps.exercise.serializers import ExerciseSerializer
from apps.workouts.models import Workout


class WorkoutsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ('id', 'name', 'is_completed')


class CreateWorkoutSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True)

    class Meta:
        model = Workout
        fields = ('name', 'description', 'duration', 'exercises')

    def create(self, validated_data):
        user = self.context['request'].user
        workout = Workout.objects.create(author=user, **validated_data)
        return workout


class DetailWorkoutSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True)
    author = AuthorExerciseSerializer()

    class Meta:
        model = Workout
        fields = '__all__'


class DestroyWorkoutSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=50)
