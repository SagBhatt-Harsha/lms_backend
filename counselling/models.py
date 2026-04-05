from django.db import models
from django.conf import settings
from mobilization.models import MobilizationRecord

# Create your models here.

class CounsellingLog(models.Model):
    STATUS_CHOICES = [
        ('Registered', 'Registered'),
        ('Not Registered', 'Not Registered'),
        ('Decision Pending', 'Decision Pending'),
    ]

    SLOT_CHOICES = [
        ('Morning', 'Morning'),
        ('Evening', 'Evening'),
    ]

    SUITABILITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    DOMAIN_CHOICES = [
        ("Digital Marketing", "Digital Marketing"),
        ("Logistics and Warehousing", "Logistics and Warehousing"), 
        ("Hospitality and Tourism", "Hospitality and Tourism"),
        ("Sales and Customer Relation", "Sales and Customer Relation"),
        ("ITES", "ITES"),
        ("Industrial Sewing", "Industrial Sewing")
    ]

    mobilization_record = models.ForeignKey(
        MobilizationRecord,
        on_delete=models.CASCADE
    )

    date = models.DateField(auto_now_add=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    slot = models.CharField(max_length=10, choices=SLOT_CHOICES, blank=True, null=True)

    domain = models.CharField(max_length=100, choices=DOMAIN_CHOICES, blank=True, null=True)

    career_interest = models.TextField(blank=True, null=True)

    aptitude_score = models.IntegerField(blank=True, null=True)

    suitability = models.CharField(max_length=10, choices=SUITABILITY_CHOICES, blank=True, null=True)

    notes = models.TextField(blank=True, null=True)

    counselled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.mobilization_record.name} - {self.status}"