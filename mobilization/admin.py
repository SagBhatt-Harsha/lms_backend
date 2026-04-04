from django.contrib import admin
from .models import MobilizationRecord, Qualification

# Register your models here.
class QualificationInline(admin.TabularInline):
    model = Qualification
    extra = 1

class MobilizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'state', 'date')
    inlines = [QualificationInline]

admin.site.register(MobilizationRecord, MobilizationAdmin)