from django.urls import path
from .views import enroll_fingerprint, verify_fingerprint, start_fingerprint, get_all_fingerprints, receive_verification

urlpatterns = [
    path('enroll_fingerprint/', enroll_fingerprint, name='enroll_fingerprint'),
    path('verify_fingerprint/', verify_fingerprint, name='verify_fingerprint'),  # This must match exactly
    path('start-fingerprint/', start_fingerprint, name='start_fingerprint'),
    path('get_all_fingerprints/', get_all_fingerprints, name='get_all_fingerprints'),
    path('receive_verification/', receive_verification, name='receive_verification'), 
]
