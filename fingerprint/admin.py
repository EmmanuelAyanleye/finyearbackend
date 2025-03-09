from django.contrib import admin
from .models import FingerprintData

@admin.register(FingerprintData)
class FingerprintDataAdmin(admin.ModelAdmin):
    list_display = ("student", "template")  # Change "fingerprint_template" to "template"
    search_fields = ("student__full_name",)
