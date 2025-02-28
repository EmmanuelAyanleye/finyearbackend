from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser
from .forms import LecturerRegistrationForm
from django.contrib.auth.decorators import user_passes_test

from django.contrib.sessions.models import Session
from django.utils import timezone

from .models import Lecturer
from .forms import CourseForm

from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Course 

from .forms import LecturerProfileUpdateForm




def group_required(group_name):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.groups.filter(name=group_name).exists():
                return redirect('home')  # Redirect to home page if not in group
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# views.py
def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

def is_lecturer(user):
    return user.is_authenticated and user.role == 'lecturer'

def is_student(user):
    return user.is_authenticated and user.role == 'student'




# 🔹 Login View
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Get the user's active session (if any)
            active_session = Session.objects.filter(
                expire_date__gte=timezone.now()
            ).filter(
                session_key=request.session.session_key
            )

            if active_session.exists():
                messages.error(request, 'You are already logged in on another tab!')
                return redirect('login')

            # Create a new session
            request.session.save()

            login(request, user)

            # Redirect user based on role
            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'student':
                return redirect('student_panel')
            elif user.role == 'lecturer':
                return redirect('lecturer_panel')

        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'home/login.html')



def logout_view(request):
    logout(request)
    request.session.pop('active_user', None)
    return redirect('login')














def index(request):
    return render(request, 'home/index.html')  # Render the homepage template


# def login(request):
#     return render(request, 'home/login.html')

def mark(request):
    return render(request, 'home/mark.html')


@user_passes_test(is_admin)
def course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        
        if form.is_valid():
            course_code = form.cleaned_data.get('course_code')
            
            # Check if the course code already exists
            if Course.objects.filter(course_code=course_code).exists():
                form.add_error('course_code', 'Course code already exists!')
                messages.error(request, 'Course code already exists!')  # Error message
            else:
                form.save()
                messages.success(request, 'Course added successfully!')  # Success message

                # Reset the form after success
                form = CourseForm()  # Clear form after successful submission
    else:
        form = CourseForm()

    return render(request, 'home/course.html', {'form': form})



@user_passes_test(is_admin)
def report(request):
    return render(request, 'home/report.html')



# @user_passes_test(is_admin)
# def settings(request):
#     return render(request, 'home/settings.html')


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='index')
def admin_dashboard(request):
    return render(request, 'home/admin_dashboard.html')


@user_passes_test(is_admin)
def admin_summary(request):
    return render(request, 'home/admin-summary.html')

# def add_lecturer(request):
#     return render(request, 'home/add-lecturer.html')


@user_passes_test(is_admin)
def add_student(request):
    return render(request, 'home/add-student.html')


@user_passes_test(is_admin)
def modify_lecturer(request):
    search_query = request.GET.get('search', '')  # Get search query from URL parameters
    lecturers = Lecturer.objects.all()

    if search_query:
        lecturers = lecturers.filter(
            full_name__icontains=search_query) | lecturers.filter(
            user__email__icontains=search_query) | lecturers.filter(
            lecturer_id__icontains=search_query
        )

    return render(request, 'home/modify-lecturer.html', {'lecturers': lecturers})

@user_passes_test(is_admin)
def delete_lecturer(request, lecturer_id):
    if request.method == "POST":
        try:
            # Fetch the Lecturer object
            lecturer = Lecturer.objects.get(id=lecturer_id)
            
            # Fetch the associated User object and delete it
            user = lecturer.user
            user.delete()
            
            # Now delete the Lecturer object
            lecturer.delete()

            return JsonResponse({"success": True})
        except Lecturer.DoesNotExist:
            return JsonResponse({"success": False, "error": "Lecturer not found"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    
    return JsonResponse({"success": False, "error": "Invalid request"})


@user_passes_test(is_admin)
def modify_lecturer_page(request, lecturer_id):
    lecturer = get_object_or_404(Lecturer, lecturer_id=lecturer_id)

    if request.method == "POST":
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        
        # Update lecturer details
        lecturer.full_name = full_name
        lecturer.phone = phone
        lecturer.user.email = email

        if password:
            # Set password if provided
            lecturer.user.set_password(password)

        # Handle profile picture upload
        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            lecturer.profile_picture = profile_picture

        # Save the changes
        lecturer.user.save()
        lecturer.save()

        # Show success message
        messages.success(request, "Lecturer details updated successfully!")
        return redirect('modify_lecturer_page', lecturer_id=lecturer_id)

    return render(request, 'home/modify-lecturer-page.html', {'lecturer': lecturer})


@user_passes_test(is_admin)
def modify_course(request):
    search_query = request.GET.get('search', '')  # Get search query from URL parameters
    courses = Course.objects.all()

    if search_query:
        courses = courses.filter(
            course_title__icontains=search_query) | courses.filter(
            course_code__icontains=search_query) | courses.filter(
            lecturer__full_name__icontains=search_query
        )

    return render(request, 'home/modify-course.html', {'courses': courses})

@user_passes_test(is_admin)
def delete_course(request, course_id):
    if request.method == "POST":
        try:
            course = Course.objects.get(id=course_id)
            course.delete()
            return JsonResponse({"success": True})
        except Course.DoesNotExist:
            return JsonResponse({"success": False, "error": "Course not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})


@user_passes_test(is_admin)
def modify_course_page(request, course_id):
    course = get_object_or_404(Course, id=course_id)  # Get the course based on the ID

    # Get the list of lecturers, departments, and semesters to populate the select fields
    lecturers = Lecturer.objects.all()
    departments = Department.objects.all()
    semesters = Semester.objects.all()

    if request.method == "POST":
        try:
            # Get form data
            course_code = request.POST.get('courseCode')
            course_title = request.POST.get('courseTitle')
            department_id = request.POST.get('department')
            semester_id = request.POST.get('semester')
            level = request.POST.get('level')
            lecturer_id = request.POST.get('lecturers')
            attendance_day = request.POST.get('attendanceDay')
            attendance_start_time = request.POST.get('attendanceStartTime')
            attendance_end_time = request.POST.get('attendanceEndTime')

            # Update course information
            course.course_code = course_code
            course.course_title = course_title
            course.department = get_object_or_404(Department, id=department_id)
            course.semester = get_object_or_404(Semester, id=semester_id)
            course.level = level
            course.lecturer = get_object_or_404(Lecturer, id=lecturer_id)
            course.attendance_day = attendance_day
            course.attendance_start_time = attendance_start_time
            course.attendance_end_time = attendance_end_time
            course.save()

            messages.success(request, "Course updated successfully!")

        except Exception as e:
            messages.error(request, f"Error updating course: {e}")

    return render(request, 'home/modify-course-page.html', {
        "course": course,
        "lecturers": lecturers,
        "departments": departments,
        "semesters": semesters
    })


@user_passes_test(is_admin)
def modify_student(request):
    return render(request, 'home/modify-student.html')


@user_passes_test(is_admin)
def modify_student_page(request):
    return render(request, 'home/modify-student-page.html')





@login_required(login_url='login')
@user_passes_test(is_lecturer, login_url='index') 
def lecturer_panel(request):
    try:
        lecturer = Lecturer.objects.get(user=request.user)
    except Lecturer.DoesNotExist:
        lecturer = None

    return render(request, "home/lecturer-panel.html", {"lecturer": lecturer}) 


@user_passes_test(is_lecturer)
def lecturer_report(request):
    
    try:
        lecturer = Lecturer.objects.get(user=request.user)
    except Lecturer.DoesNotExist:
        lecturer = None

    return render(request, "home/lecturer-report.html", {"lecturer": lecturer}) 


@user_passes_test(is_lecturer)
def lecturer_summary(request):
    
    try:
        lecturer = Lecturer.objects.get(user=request.user)
    except Lecturer.DoesNotExist:
        lecturer = None

    return render(request, "home/lecturer-summary.html", {"lecturer": lecturer}) 


@user_passes_test(is_lecturer)
def manage_class(request):
    # Get the lecturer object
    lecturer = Lecturer.objects.get(user=request.user)

    # Fetch courses assigned to the logged-in lecturer
    courses = Course.objects.filter(lecturer=lecturer)

    return render(request, 'home/manage-class.html', {'courses': courses}) 


@user_passes_test(is_lecturer)
def modify_class(request, course_id):
    course_allocation = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_day = data.get('day')
            new_start_time = data.get('start_time')
            new_end_time = data.get('end_time')

            # Validate data
            if not new_day or not new_start_time or not new_end_time:
                return JsonResponse({'error': 'All fields are required'}, status=400)

            # Update course allocation
            course_allocation.attendance_day = new_day
            course_allocation.attendance_start_time = new_start_time
            course_allocation.attendance_end_time = new_end_time
            course_allocation.save()

            return JsonResponse({'message': 'Class updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'home/modify-class.html', {
        'course': course_allocation,  # ✅ Send course details to the template
    })

@user_passes_test(is_lecturer)
def modify_profile(request):
    try:
        lecturer = Lecturer.objects.get(user=request.user)
    except Lecturer.DoesNotExist:
        lecturer = None

    if request.method == 'POST':
        form = LecturerProfileUpdateForm(request.POST, request.FILES, instance=lecturer)
        
        if form.is_valid():
            form.save(user=request.user)  # ✅ Pass 'user' explicitly
            messages.success(request, "Profile updated successfully!")
            
            # Reset the form with the updated lecturer instance
            form = LecturerProfileUpdateForm(instance=lecturer)

        else:
            messages.error(request, "There was an error updating your profile. Please check the form.")

    else:
        form = LecturerProfileUpdateForm(instance=lecturer)

    return render(request, "home/modify-profile.html", {"form": form, "lecturer": lecturer})

@user_passes_test(is_lecturer)
def profile(request):
    try:
        lecturer = Lecturer.objects.get(user=request.user)  # Get lecturer details linked to the logged-in user
    except Lecturer.DoesNotExist:
        lecturer = None  # If no lecturer profile exists

    return render(request, "home/profile.html", {"lecturer": lecturer})





@user_passes_test(is_student)
def student_summary(request):
    return render(request, 'home/student-summary.html')



@user_passes_test(is_student)
def student_report(request):
    return render(request, 'home/student-report.html')



@user_passes_test(is_student)
def student_modify(request):
    return render(request, 'home/student-modify.html')


@user_passes_test(is_student)
def student_profile(request):
    return render(request, 'home/student-profile.html')


@login_required(login_url='login')
@user_passes_test(is_student, login_url='index') 
def student_panel(request):
    return render(request, 'home/student-panel.html')




























from .forms import LecturerRegistrationForm


@user_passes_test(is_admin)
def add_lecturer(request):
    if request.method == 'POST':
        form = LecturerRegistrationForm(request.POST, request.FILES)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            lecturer_id = form.cleaned_data['lecturer_id']  # Grab the lecturer_id
            
            # Check if the email already exists
            if CustomUser.objects.filter(email=email).exists():  # FIX: Use 'email' instead of 'user.email'
                form.add_error('email', 'A lecturer with this email already exists.')  # Add error to the email field
                messages.error(request, 'A lecturer with this email already exists.')  # General error message
            # Check if the lecturer_id already exists
            elif Lecturer.objects.filter(lecturer_id=lecturer_id).exists():
                form.add_error('lecturer_id', 'Lecturer ID already exists!')  # Add error to the lecturer_id field
                messages.error(request, 'Lecturer ID already exists!')  # General error message
            else:
                # If the email and lecturer_id are unique, proceed to save
                user = CustomUser.objects.create_user(
                    email=email,
                    password=form.cleaned_data['password'],
                    role='lecturer'
                )
                lecturer = form.save(commit=False)
                lecturer.user = user
                lecturer.save()
                messages.success(request, "Lecturer added successfully!")
                
                # Reset the form after success
                form = LecturerRegistrationForm()  # Clear form after successful submission
        else:
            # If the form is not valid, show the generic error message
            messages.error(request, "Error adding lecturer. Please check the form.")

    else:
        form = LecturerRegistrationForm()

    return render(request, 'home/add-lecturer.html', {'form': form})








from .models import AcademicSession, Semester, Department
from .forms import AcademicSessionForm, SemesterForm, DepartmentForm
@user_passes_test(is_admin)
def settings(request):
    if request.method == "POST":
        # Handle adding new sessions, semesters, or departments
        if 'add_session' in request.POST:
            session_name = request.POST.get('session_name')
            AcademicSession.objects.create(name=session_name)
        elif 'add_semester' in request.POST:
            semester_name = request.POST.get('semester_name')
            Semester.objects.create(name=semester_name)
        elif 'add_department' in request.POST:
            department_name = request.POST.get('department_name')
            Department.objects.create(name=department_name)

    # Handle modifications and deletions
    if request.method == "GET":
        if 'delete_session' in request.GET:
            session_id = request.GET.get('delete_session')
            AcademicSession.objects.get(id=session_id).delete()
        elif 'delete_semester' in request.GET:
            semester_id = request.GET.get('delete_semester')
            Semester.objects.get(id=semester_id).delete()
        elif 'delete_department' in request.GET:
            department_id = request.GET.get('delete_department')
            Department.objects.get(id=department_id).delete()

    # Get all the sessions, semesters, and departments
    sessions = AcademicSession.objects.all()
    semesters = Semester.objects.all()
    departments = Department.objects.all()

    return render(request, 'home/settings.html', {
        'sessions': sessions,
        'semesters': semesters,
        'departments': departments
    })