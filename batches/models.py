from django.db import models
from teachers.models import Teacher
from counselling.models import CounsellingLog

# Create your models here.

class Batch(models.Model):

    SLOT_CHOICES = CounsellingLog.SLOT_CHOICES

    DOMAIN_CHOICES = Teacher.DOMAIN_CHOICES  # reuse from Teacher

    name = models.CharField(max_length=150)
    slot = models.CharField(max_length=10, choices=SLOT_CHOICES)
    domain = models.CharField(max_length=100, choices=DOMAIN_CHOICES)

    start_date = models.DateField()
    end_date = models.DateField()

    start_time = models.TimeField()
    end_time = models.TimeField()

    capacity = models.PositiveIntegerField()

    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    # 

    def __str__(self):
        return self.name

    # clean() Method is used for Validation before Saving for POST requests.
    def clean(self):
        from django.core.exceptions import ValidationError

        if self.end_date < self.start_date:
            raise ValidationError("End date must be after start date")

        if self.end_time <= self.start_time:
            raise ValidationError("End time must be greater than start time")

        if self.capacity < 1:
            raise ValidationError("Capacity must be at least 1")