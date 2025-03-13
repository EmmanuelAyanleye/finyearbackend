from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import subprocess
from home.models import Student
from .models import FingerprintData  
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
import os

@csrf_exempt
def get_csrf_token(request):
    return JsonResponse({"csrftoken": get_token(request)})


@api_view(['POST'])
def enroll_fingerprint(request):
    try:
        data = request.data
        student_id = data.get('student_id')
        fingerprint_data = data.get('fingerprint')

        if not student_id or not fingerprint_data:
            return Response({"error": "Missing required fields"}, status=400)

        FingerprintData.objects.create(student_id=student_id, template=fingerprint_data)
        return Response({"message": "Fingerprint enrolled successfully"}, status=201)

    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def receive_verification(request):
    data = request.data
    matric_number = data.get("matric_number")

    if not matric_number:
        return Response({"error": "Matric number is missing"}, status=400)

    try:
        student = Student.objects.get(matric_number=matric_number)

        # Update student attendance (Example)
        student.attendance_status = "Present"
        student.save()

        return Response({
            "status": "verified",
            "message": f"Student {student.full_name} verified",
            "student": student.matric_number
        })

    except Student.DoesNotExist:
        return Response({"error": "Student not found"}, status=404)



from rest_framework.authentication import BasicAuthentication, SessionAuthentication

from rest_framework.authentication import BasicAuthentication, SessionAuthentication

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def verify_fingerprint(request):
    try:
        data = json.loads(request.body)
        scanned_template = data.get("fingerprint")
        student_id = data.get("student_id")

        if not scanned_template:
            return JsonResponse({"status": "error", "message": "Missing fingerprint data."}, status=400)

        stored_fingerprints = FingerprintData.objects.values_list("template", "student_id")

        for stored_template, stored_student_id in stored_fingerprints:
            if scanned_template.strip() == stored_template.strip():
                student = Student.objects.get(id=stored_student_id)

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
@permission_classes([AllowAny])
def get_all_fingerprints(request):
    fingerprints = FingerprintData.objects.select_related('student').all()
    data = [
        {
            "matric_number": fp.student.matric_number,  # Send matric_number instead of student_id
            "template": fp.template,
        }
        for fp in fingerprints
    ]
    return Response({"status": "success", "fingerprints": data})



@csrf_exempt
def start_fingerprint(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            student_id = data.get("student_id")
            mode = data.get("operation_mode")

            if not student_id or not mode:
                return JsonResponse({"status": "error", "message": "Missing student_id or operation_mode"}, status=400)

            # Define the correct executable path based on mode
            app_path = (
                r"C:\Users\EMMANUEL AYANLEYE\Downloads\EnrollFinger\EnrollFinger\bin\Debug\EnrollFinger.exe"
                if mode == "enroll"
                else r"C:\Users\EMMANUEL AYANLEYE\Downloads\VerifyFinger\VerifyFinger\bin\Debug\VerifyFinger.exe"
            )

            # Ensure the executable exists
            if not os.path.exists(app_path):
                return JsonResponse({"status": "error", "message": f"Executable not found: {app_path}"}, status=500)

            print(f"Running: {app_path} with student_id: {student_id}")  # Debugging output

            # Run the fingerprint scanning application
            process = subprocess.run(
                [app_path, str(student_id)], 
                capture_output=True,
                text=True
            )

            if process.returncode != 0:
                return JsonResponse({"status": "error", "message": f"Process failed: {process.stderr}"}, status=500)

            fingerprint_template = process.stdout.strip()
            if not fingerprint_template:
                return JsonResponse({"status": "error", "message": "No fingerprint data received"}, status=500)

            return JsonResponse({"status": "success", "fingerprint": fingerprint_template})

        except Exception as e:
            print(f"Exception: {str(e)}")  # Debugging
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)