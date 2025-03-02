from django.urls import path
from .views import enroll_fingerprint

urlpatterns = [
    path('enroll_fingerprint/', enroll_fingerprint, name='enroll_fingerprint'),
]
