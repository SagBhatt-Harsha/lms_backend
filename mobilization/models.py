from django.db import models
from django.conf import settings

# Create your models here.

class MobilizationRecord(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    ]

    name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    dob = models.DateField()

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    caste = models.CharField(max_length=10)

    nationality = models.CharField(max_length=50, default="Indian")

    mobile = models.CharField(max_length=10, unique=True) 
    # No 2 Mob Recs will have same mobile numbers.
    email = models.EmailField(blank=True, null=True)

    address = models.TextField()
    state = models.CharField(max_length=50)
    pin = models.CharField(max_length=6)

    landmark = models.CharField(max_length=100, blank=True, null=True)

    aadhar_no = models.CharField(max_length=14, blank=True, null=True)
    pan_no = models.CharField(max_length=10, blank=True, null=True)

    occupation = models.CharField(max_length=20)

    family_income = models.DecimalField(max_digits=10, decimal_places=2)
    personal_income = models.DecimalField(max_digits=10, decimal_places=2)

    date = models.DateField(auto_now_add=True)

    created_by = models.ForeignKey(
        # Current logged-in Authenticated User tracked by Token is denoted as Creator of this Mobilization Record.
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.name} - {self.mobile}"


class Qualification(models.Model):
    record = models.ForeignKey(
        MobilizationRecord,
        related_name='qualifications', # Means record.qualifications.all()
        on_delete=models.CASCADE
    )
    # Above lines create a One-to-Many Relationship: One MobilizationRecord → Many Qualifications. 
    # In DB, Each Qualification row/tuple will have a MobilizationRecord Id(Fk) assoc. with them.

    sl_no = models.IntegerField()
    exam_name = models.CharField(max_length=100)
    board = models.CharField(max_length=100)
    year_of_passing = models.CharField(max_length=4)
    grade = models.CharField(max_length=20)

    def __str__(self):
        return self.exam_name