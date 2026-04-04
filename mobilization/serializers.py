from rest_framework import serializers
from .models import MobilizationRecord, Qualification


class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = '__all__'
        extra_kwargs = {
            'record': {'read_only': True}
            # 'record' is simply used as FK for establishing one-to-many Rel. with MobilizationRec Model.So, this field does not need to be inputted by user. 
        }

class MobilizationSerializer(serializers.ModelSerializer):
    qualifications = QualificationSerializer(many=True)

    class Meta:
        model = MobilizationRecord
        fields = '__all__'
        extra_kwargs = {
            'created_by': {'read_only': True}
        }

    def create(self, validated_data):
        # For POST.
        qualifications_data = validated_data.pop('qualifications')

        record = MobilizationRecord.objects.create(**validated_data)

        for q in qualifications_data:
            Qualification.objects.create(record=record, **q)

        return record
    
    
    def update(self, instance, validated_data):
        qualifications_data = validated_data.pop('qualifications', None)

        # Update main record
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update qualifications
        if qualifications_data:
            # Delete old qualifications
            instance.qualifications.all().delete()

            # Create new ones
            for q in qualifications_data:
                q.pop('record', None)  # remove if present
                Qualification.objects.create(record=instance, **q)

        return instance