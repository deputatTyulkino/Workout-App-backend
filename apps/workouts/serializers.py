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
        for ex_data in exercises:
            try:
                exercise = Exercise.objects.get(id=ex_data.id)
            except Exercise.DoesNotExist:
                raise serializers.ValidationError('Not Found exercise with this ID')
            workout.exercises.add(exercise)
        return workout


class DetailWorkoutSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True)
    author = AuthorExerciseSerializer()

    class Meta:
        model = Workout
        fields = '__all__'


class UpdateWorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ('name', 'description', 'duration', 'is_completed', 'is_public')


class DestroyWorkoutSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=50)
