from django.db import models
from home.models import Student  # Importing Student from home app

class FingerprintData(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    fingerprint_data = models.TextField()  # Storing Base64 fingerprint template

    def __str__(self):
        return f"Fingerprint for {self.student.full_name}"
