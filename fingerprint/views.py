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


@csrf_exempt
@csrf_exempt
def start_enroll(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

    try:
        data = json.loads(request.body)
        student_id = data.get("student_id")

        if not student_id:
            return JsonResponse({"status": "error", "message": "Missing student_id"}, status=400)

        # Path to your C# fingerprint enrollment application
        app_path = r"C:\Users\EMMANUEL AYANLEYE\Downloads\EnrollFinger\EnrollFinger\bin\Debug\EnrollFinger.exe"

        if not os.path.exists(app_path):
            return JsonResponse({"status": "error", "message": "Fingerprint enrollment software not found"}, status=500)

        # Run the C# application with student ID
        process = subprocess.run(
            [app_path, str(student_id)],
            capture_output=True,
            text=True,
            check=True
        )

        if process.returncode == 0 and process.stdout.strip():
            return JsonResponse({
                "status": "success",
                "fingerprint": process.stdout.strip()
            })
        else:
            return JsonResponse({
                "status": "error",
                "message": "No fingerprint data received"
            }, status=500)

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": f"Enrollment failed: {str(e)}"
        }, status=500)



from rest_framework.authentication import BasicAuthentication, SessionAuthentication

from rest_framework.authentication import BasicAuthentication, SessionAuthentication

from django.views.decorators.csrf import csrf_exempt




import os
import json
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from home.models import Student

    


@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_fingerprints(request):
    fingerprints = FingerprintData.objects.select_related('student').all()
    data = [
        {
            "matric_number": fp.student.matric_number,
            "template": fp.template,
        }
        for fp in fingerprints
    ]
    return Response({"status": "success", "fingerprints": data})


import os
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_fingerprint(request):
    try:
        data = json.loads(request.body)
        matric_number = data.get("matric_number")

        if not matric_number:
            return JsonResponse({"status": "error", "message": "No matric number provided"}, status=400)

        print(f"Received matric number: {matric_number}")

        # Retrieve the student with the matching matric number
        student = Student.objects.filter(matric_number=matric_number).first()

        if not student:
            return JsonResponse({"status": "error", "message": "Student not recognized"}, status=404)

        print(f"Matched student: {student.full_name}")

        return JsonResponse({
            "status": "success",
            "name": student.full_name,
            "department": student.department.name,
            "matric_number": student.matric_number,
            "level": student.get_level_display(),
            "gender": student.user.get_gender_display()  # Assuming gender is a field in CustomUser
        })

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
    

from home.models import CustomUser, Student
from django.core.cache import cache
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from home.models import Student, CustomUser
import json

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def receive_verification(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            matric_number = data.get('matric_number')
            
            if not matric_number:
                return JsonResponse({"status": "error", "message": "No matric number received"}, status=400)
            
            student = Student.objects.filter(matric_number=matric_number).first()
            if not student:
                return JsonResponse({"status": "error", "message": "Student not found"}, status=404)
            
            # Fix gender display
            gender_display = "Male" if student.gender == "M" else "Female"
            
            student_details = {
                "status": "success",
                "name": student.full_name,
                "department": student.department.name,
                "matric_number": student.matric_number,
                "level": student.get_level_display(),
                "gender": gender_display  # Use the correct gender display
            }
            
            request.session['verified_student'] = student_details
            return JsonResponse(student_details)
            
        else:
            # Handle GET request from frontend
            stdout = request.session.get('stdout_data')
            if stdout:
                # Clear the session data
                del request.session['stdout_data']
                
                # Find student by matric number from stdout
                student = Student.objects.filter(matric_number=stdout.strip()).first()
                if student:
                    student_details = {
                        "status": "success",
                        "name": student.full_name,
                        "department": student.department.name,
                        "matric_number": student.matric_number,
                        "level": student.get_level_display(),
                        "gender": "Male" if student.user.gender == "M" else "Female"
                    }
                    return JsonResponse(student_details)
            
            return JsonResponse({"status": "pending", "message": "No verification data found"})

    except Exception as e:
        print(f"Error in receive_verification: {str(e)}")
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def start_verify(request):
    try:
        print("Starting fingerprint scan...")
        app_path = r"C:\Users\EMMANUEL AYANLEYE\Downloads\VerifyFinger\VerifyFinger\bin\Debug\VerifyFinger.exe"

        if not os.path.exists(app_path):
            return JsonResponse({
                "status": "error", 
                "message": "Fingerprint verification software not found"
            }, status=500)

        process = subprocess.Popen(
            [app_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate()
        print(f"Process completed with return code: {process.returncode}")
        print(f"stdout: {stdout}")
        print(f"stderr: {stderr}")

        if process.returncode == 0 and stdout.strip():
            # Store the stdout in session for later retrieval
            request.session['stdout_data'] = stdout.strip()
            return JsonResponse({"status": "success", "message": "Verification completed"})
        else:
            return JsonResponse({
                "status": "error",
                "message": f"Verification failed: {stderr or 'No output received'}"
            }, status=500)

    except Exception as e:
        print(f"Error in start_verify: {str(e)}")
        return JsonResponse({
            "status": "error",
            "message": f"Failed to start fingerprint verification: {str(e)}"
        }, status=500)