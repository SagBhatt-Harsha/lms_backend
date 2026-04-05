from django.contrib import admin
from .models import Teacher

# Register your models here.

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):

    # list_display : Columns to be shown in TeacherAdmin admin panel.
    list_display = (
        'id',
        'name',
        'domain',
        'email',
        'phone'
    )

    search_fields = (
        'name',
        'domain',
        'email'
    )

    list_filter = (
        'domain',
    )