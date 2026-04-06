from django.db import models
from counselling.models import CounsellingLog
from batches.models import Batch
from django.conf import settings

# Create your models here.

class Trainee(models.Model):

    counselling_log = models.OneToOneField(CounsellingLog, on_delete=models.CASCADE)

    registered_date = models.DateField(auto_now_add=True)

    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True)

    # DENORMALIZED FIELDS.Stored again for better performance.
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    contact = models.CharField(max_length=10)

    slot = models.CharField(max_length=10)
    domain = models.CharField(max_length=100)

    education = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    registered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name