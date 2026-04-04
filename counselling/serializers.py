from rest_framework import serializers
from .models import CounsellingLog


class CounsellingSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='mobilization_record.name', read_only=True)
    mobile = serializers.CharField(source='mobilization_record.mobile', read_only=True)
    gender = serializers.CharField(source='mobilization_record.gender', read_only=True)
    # Above 3 Fields are Derived Fields. mobilization_record is the FK in the CounsellingLog Model. mobilization_record is nothing but the id of req. mobilization Record in the MobilizationRecord Table/Model.


    class Meta:
        model = CounsellingLog
        fields = '__all__'
        extra_kwargs = {
            'counselled_by': {'read_only': True}
        }

    def validate(self, data):
        status = data.get('status')
        slot = data.get('slot')
        domain = data.get('domain')
        aptitude_score = data.get('aptitude_score')

        # If status==reg., then domain and slot are required to have Values. Can't be Null then.
        if status == 'Registered':
            if not slot:
                raise serializers.ValidationError("Slot is required when status is Registered")
            if not domain:
                raise serializers.ValidationError("Domain is required when status is Registered")

        
        if aptitude_score is not None:
            if not (0 <= aptitude_score <= 100):
                raise serializers.ValidationError("Aptitude score must be between 0 and 100")

        return data