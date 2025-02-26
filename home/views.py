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
    return render(request, 'home/modify-lecturer.html')


@user_passes_test(is_admin)
def modify_lecturer_page(request):
    return render(request, 'home/modify-lecturer-page.html')


@user_passes_test(is_admin)
def modify_course(request):
    return render(request, 'home/modify-course.html')


@user_passes_test(is_admin)
def modify_course_page(request):
    return render(request, 'home/modify-course-page.html')


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
    try:
        lecturer = Lecturer.objects.get(user=request.user)
    except Lecturer.DoesNotExist:
        lecturer = None

    return render(request, "home/manage-class.html", {"lecturer": lecturer}) 


@user_passes_test(is_lecturer)
def modify_class(request):
    
    try:
        lecturer = Lecturer.objects.get(user=request.user)
    except Lecturer.DoesNotExist:
        lecturer = None

    return render(request, "home/modify-class.html", {"lecturer": lecturer}) 


@user_passes_test(is_lecturer)
def modify_profile(request):
    lecturer = Lecturer.objects.get(user=request.user)

    try:
        lecturer = Lecturer.objects.get(user=request.user)
    except Lecturer.DoesNotExist:
        lecturer = None

    if request.method == 'POST':
        form = LecturerProfileUpdateForm(request.POST, request.FILES, instance=lecturer)
        
        if form.is_valid():
            form.save(user=request.user)
            messages.success(request, "Profile updated successfully!")
            return redirect('lecturer_panel')

        else:
            messages.error(request, "There was an error updating your profile.")
    
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
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "A lecturer with this email already exists.")  # ✅ Show specific error
            else:
                user = CustomUser.objects.create_user(
                    email=email,
                    password=form.cleaned_data['password'],
                    role='lecturer'
                )
                lecturer = form.save(commit=False)
                lecturer.user = user
                lecturer.save()
                messages.success(request, "Lecturer added successfully!")
                return redirect('add_lecturer')  # ✅ Stay on the same page
        else:
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