from django.contrib import admin
from .models import Trainee

# Register your models here.

@admin.register(Trainee)
class TraineeAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'domain',
        'slot',
        'batch',
        'registered_date'
    )

    search_fields = (
        'name',
        'contact'
    )

    list_filter = (
        'domain',
        'slot'
    )

    autocomplete_fields = ('batch', 'counselling_log')