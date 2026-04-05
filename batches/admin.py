from django.contrib import admin
from .models import Batch

# Register your models here.

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'domain',
        'slot',
        'start_date',
        'end_date',
        'capacity',
        'teacher'
    )

    list_filter = (
        'domain',
        'slot'
    )

    search_fields = (
        'name',
        'domain'
    )

    autocomplete_fields = ('teacher',)