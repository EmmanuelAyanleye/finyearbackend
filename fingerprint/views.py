from django.http import JsonResponse
import base64
import json
from home.models import Student


def enroll_fingerprint(request):
    if request.method == 'POST':
        try:
            # Extract data from the request body
            data = json.loads(request.body)
            student_id = data.get('student_id')
            fingerprint_base64 = data.get('fingerprint')

            if not student_id or not fingerprint_base64:
                return JsonResponse({"error": "Missing student_id or fingerprint"}, status=400)

            # Decode the Base64 fingerprint data
            try:
                fingerprint_data = base64.b64decode(fingerprint_base64)
            except Exception as e:
                return JsonResponse({"error": "Invalid fingerprint data"}, status=400)

            # Assuming you have a Student model where you can save the fingerprint data
            try:
                student = Student.objects.get(id=student_id)
                student.fingerprint_data = fingerprint_base64  # Store the Base64 string
                student.save()
                return JsonResponse({"message": "Fingerprint enrolled successfully"})
            except Student.DoesNotExist:
                return JsonResponse({"error": "Student not found"}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)
