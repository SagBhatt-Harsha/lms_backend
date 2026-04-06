from rest_framework import serializers
from datetime import date

from .models import Trainee
from counselling.models import CounsellingLog


class TraineeSerializer(serializers.ModelSerializer):

    # COMPUTED FIELD
    age = serializers.SerializerMethodField()

    class Meta:
        model = Trainee
        fields = '__all__'
        extra_kwargs = {
            'registered_by': {'read_only': True},
            'name': {'read_only': True},
            'gender': {'read_only': True},
            'contact': {'read_only': True},
            'address': {'read_only': True},    
            'education': {'read_only': True}
        }

    # AGE CALCULATION
    def get_age(self, obj):
        dob = obj.counselling_log.mobilization_record.dob

        if not dob:
            return None

        today = date.today()
        age = today.year - dob.year

        if (today.month, today.day) < (dob.month, dob.day):
            age -= 1

        return age

    # CREATE METHOD - for Post
    def create(self, validated_data):
        counselling_log = validated_data.get('counselling_log')

        # VALIDATION 1
        if counselling_log.status != "Registered":
            raise serializers.ValidationError(
                "Only Registered candidates can be onboarded"
            )

        # VALIDATION 2
        if Trainee.objects.filter(counselling_log=counselling_log).exists():
            raise serializers.ValidationError(
                "Trainee already exists for this counselling log"
            )

        mobilization = counselling_log.mobilization_record

        trainee = Trainee.objects.create(
            counselling_log=counselling_log,

            # USER INPUT
            slot=validated_data.get('slot'),
            domain=validated_data.get('domain'),

            # AUTO-FILLED (DENORMALIZED)
            name=mobilization.name,
            gender=mobilization.gender,
            contact=mobilization.mobile,
            address=mobilization.address,
            education=self.get_highest_education(mobilization),

            registered_by=self.context['request'].user
        )

        return trainee

    # EDUCATION HELPER
    def get_highest_education(self, mobilization):
        qualifications = mobilization.qualifications.all()

        if qualifications.exists():
            return qualifications.order_by('-sl_no').first().exam_name

        return None