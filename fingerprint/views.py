from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import base64
import subprocess
from home.models import Student
from .models import FingerprintData  # Fingerprint model is in fingerprint app

@csrf_exempt  # Disable CSRF for API testing (not recommended for production)
def enroll_fingerprint(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Read JSON body
            student_id = data.get("student_id")
            fingerprint_data = data.get("fingerprint")

            if not student_id or not fingerprint_data:
                return JsonResponse({"status": "error", "message": "Missing student_id or fingerprint"}, status=400)

            student = Student.objects.get(id=student_id)
            fp_entry, created = FingerprintData.objects.get_or_create(student=student)
            fp_entry.fingerprint_data = fingerprint_data
            fp_entry.save()

            return JsonResponse({"status": "success", "message": "Fingerprint enrolled!"})

        except Student.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Student not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)


@csrf_exempt
def verify_fingerprint(request):
    if request.method == "POST":
        data = json.loads(request.body)
        student_id = data.get("student_id")
        fingerprint = data.get("fingerprint")

        try:
            stored_data = FingerprintData.objects.get(student__matric_number=student_id)
            stored_template = stored_data.fingerprint_data

            if fingerprint == stored_template:
                return JsonResponse({"message": "Fingerprint matched! Attendance marked."}, status=200)
            else:
                return JsonResponse({"message": "Fingerprint did not match!"}, status=400)
        except FingerprintData.DoesNotExist:
            return JsonResponse({"message": "No fingerprint found for this student."}, status=404)

import subprocess
import json
from django.http import JsonResponse

import subprocess
from django.http import JsonResponse

def start_fingerprint(request):
    student_id = request.GET.get("student_id")  # Get the matric number

    if not student_id:
        return JsonResponse({"status": "error", "error": "Missing student ID"}, status=400)

    try:
        app_path = r"C:\Users\EMMANUEL AYANLEYE\Downloads\FingerprintAPP\FingerprintAPP\bin\Debug\FingerprintAPP.exe"

        # Use student_id (matric number) as a string
        process = subprocess.Popen([app_path, str(student_id)], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if error:
            return JsonResponse({"status": "error", "message": error.decode()}, status=500)

        # Return fingerprint template if successful
        fingerprint_template = output.decode().strip()
        return JsonResponse({"status": "success", "fingerprint": fingerprint_template})

    except Exception as e:
        return JsonResponse({"status": "error", "error": str(e)}, status=500)
