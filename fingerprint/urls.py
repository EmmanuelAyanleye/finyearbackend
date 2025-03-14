from django.urls import path
from .views import (
    enroll_fingerprint, verify_fingerprint, start_enroll, start_verify, 
    get_all_fingerprints, receive_verification, get_csrf_token
)

urlpatterns = [
    path('enroll_fingerprint/', enroll_fingerprint, name='enroll_fingerprint'),
    path('verify_fingerprint/', verify_fingerprint, name='verify_fingerprint'), 
    path("start_enroll/", start_enroll, name="start_enroll"),
    path('start_verify/', start_verify, name='start_verify'),
    path('get_all_fingerprints/', get_all_fingerprints, name='get_all_fingerprints'),
    path('receive_verification/', receive_verification, name='receive_verification'),
    path('csrf_token/', get_csrf_token, name='get_csrf_token'),
]


from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/fingerprint/$', consumers.FingerprintConsumer.as_asgi()),
]
