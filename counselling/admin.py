from django.contrib import admin
from .models import CounsellingLog

# Register your models here.

@admin.register(CounsellingLog)
class CounsellingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'mobilization_record',
        'status',
        'slot',
        'domain',
        'counselled_by',
        'date'
    )

    list_filter = (
        'status',
        'slot',
        'domain',
        'date'
    )

    search_fields = (
        'mobilization_record__name',
        'mobilization_record__mobile',
        'domain'
    )

    readonly_fields = ('date',)

    autocomplete_fields = ('mobilization_record', 'counselled_by')