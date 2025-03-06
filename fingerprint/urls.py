from django.urls import path
from .views import enroll_fingerprint, verify_fingerprint, start_fingerprint

urlpatterns = [
    path('enroll_fingerprint/', enroll_fingerprint, name='enroll_fingerprint'),
    path('verify_fingerprint/', verify_fingerprint, name='verify_fingerprint'),
    path('start-fingerprint/', start_fingerprint, name='start_fingerprint')

]
