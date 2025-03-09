from django.db import models

class FingerprintData(models.Model):
    student = models.ForeignKey('home.Student', on_delete=models.CASCADE)  # Reference to student
    template = models.TextField()  # Storing fingerprint data as Base64 or another format

    def __str__(self):
        return f"Fingerprint of {self.student}"
