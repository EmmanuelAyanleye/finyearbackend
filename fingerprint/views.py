from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import base64
import subprocess
from home.models import Student
from .models import FingerprintData  
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def enroll_fingerprint(request):
    print("Received Data:", request.body)  # Debugging line

    try:
        data = request.data
        print("Parsed Data:", data)  # Debugging line

        student_id = data.get('student_id')
        fingerprint_data = data.get('fingerprint')  # Fix field name here

        if not student_id or not fingerprint_data:
            return Response({"error": "Missing required fields"}, status=400)

        # Save to database
        FingerprintData.objects.create(student_id=student_id, template=fingerprint_data)

        return Response({"message": "Fingerprint enrolled successfully"}, status=201)

    except Exception as e:
        print("Error:", str(e))  # Debugging line
        return Response({"error": str(e)}, status=400)



import logging
logger = logging.getLogger(__name__)

from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)

@csrf_exempt
def receive_verification(request):
    try:
        data = json.loads(request.body.decode("utf-8"))  # Decode request body
        print("Received Data in Django:", data)  # Debugging

        if "fingerprint_data" not in data or "student_id" not in data:
            return JsonResponse({"error": "Missing required fields"}, status=400)

        return JsonResponse({"status": "Fingerprint received!"})
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)



@api_view(['POST'])
@csrf_exempt
def verify_fingerprint(request):
    try:
        data = json.loads(request.body)
        scanned_template = data.get("fingerprint")

        if not scanned_template:
            return JsonResponse({"status": "error", "message": "Missing fingerprint data."}, status=400)

        stored_fingerprints = FingerprintData.objects.values_list("template", "student_id")

        for stored_template, student_id in stored_fingerprints:
            if scanned_template.strip() == stored_template.strip():
                student = Student.objects.get(id=student_id)

                return JsonResponse({
                    "status": "success",
                    "message": "Fingerprint matched!",
                    "student_id": student.id,
                    "name": student.full_name,
                    "matric_number": student.matric_number,
                    "department": student.department.name,
                    "level": student.level,
                    "gender": student.gender
                })

        return JsonResponse({"status": "error", "message": "Fingerprint not recognized."}, status=401)

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)



@api_view(['GET'])
def get_all_fingerprints(request):
    fingerprints = FingerprintData.objects.all()
    fingerprint_list = [
        {"student_id": f.student.id, "template": f.template} for f in fingerprints
    ]
    
    return JsonResponse({"status": "success", "fingerprints": fingerprint_list})



import subprocess
import json
from django.http import JsonResponse

import subprocess
from django.http import JsonResponse


from django.views.decorators.csrf import csrf_exempt
import logging
logger = logging.getLogger(__name__)

@csrf_exempt
def start_fingerprint(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            student_id = data.get("student_id")
            mode = data.get("operation_mode")

            logger.debug(f"Received data: {data}")

            app_path = r"C:\Users\EMMANUEL AYANLEYE\Downloads\EnrollFinger\EnrollFinger\bin\Debug\EnrollFinger.exe" if mode == "enroll" else r"C:\Users\EMMANUEL AYANLEYE\Downloads\VerifyFinger\VerifyFinger\bin\Debug\VerifyFinger.exe"

            process = subprocess.Popen([app_path, str(student_id)], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, error = process.communicate()

            if error:
                logger.error(f"Error in fingerprint scanning: {error}")
                return JsonResponse({"status": "error", "message": error}, status=500)

            fingerprint_template = output.strip()
            if not fingerprint_template:
                logger.error("No fingerprint data returned from the C# application.")
                return JsonResponse({"status": "error", "message": "No fingerprint data received"}, status=500)

            return JsonResponse({"status": "success", "fingerprint": fingerprint_template})

        except Exception as e:
            logger.error(f"Error in start_fingerprint: {e}")
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
