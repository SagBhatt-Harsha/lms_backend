from rest_framework import serializers
from .models import Batch
from teachers.models import Teacher


class TeacherMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name']
        # We want teacher id and name in Response acc. to teacher id unputted in Request.


class BatchSerializer(serializers.ModelSerializer):
    teacher = TeacherMiniSerializer(read_only=True)
    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(), source='teacher',
        write_only=True, required=False
    )
    # Above two lines :- when we Input teacher_id in Request, we get teacher_id & name in Response.

    enrolled_count = serializers.SerializerMethodField()

    class Meta:
        model = Batch
        fields = '__all__'

    def get_enrolled_count(self, obj):
        # Reverse relation from onboarding App.
        return obj.trainee_set.count() if hasattr(obj, 'trainee_set') else 0

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError("End date must be >= start date")

        if start_time and end_time and end_time <= start_time:
            raise serializers.ValidationError("End time must be greater")

        return data