from django.contrib import admin
from .models import FingerprintData

@admin.register(FingerprintData)
class FingerprintDataAdmin(admin.ModelAdmin):
    list_display = ("student", "fingerprint_data")  # Show in admin panel
    search_fields = ("student__full_name",)

