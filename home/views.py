from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser
from .forms import LecturerRegistrationForm



# 🔹 Login View
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'student':
                return redirect('student_panel')
            elif user.role == 'lecturer':
                return redirect('lecturer_panel')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'home/login.html')



@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')














def index(request):
    return render(request, 'home/index.html')  # Render the homepage template


# def login(request):
#     return render(request, 'home/login.html')

def mark(request):
    return render(request, 'home/mark.html')



def course(request):
    return render(request, 'home/course.html')




def report(request):
    return render(request, 'home/report.html')




def settings(request):
    return render(request, 'home/settings.html')



@login_required(login_url='login')
def admin_dashboard(request):
    return render(request, 'home/admin_dashboard.html')



def admin_summary(request):
    return render(request, 'home/admin-summary.html')

# def add_lecturer(request):
#     return render(request, 'home/add-lecturer.html')



def add_student(request):
    return render(request, 'home/add-student.html')



def modify_lecturer(request):
    return render(request, 'home/modify-lecturer.html')



def modify_lecturer_page(request):
    return render(request, 'home/modify-lecturer-page.html')



def modify_course(request):
    return render(request, 'home/modify-course.html')



def modify_course_page(request):
    return render(request, 'home/modify-course-page.html')



def modify_student(request):
    return render(request, 'home/modify-student.html')



def modify_student_page(request):
    return render(request, 'home/modify-student-page.html')





@login_required(login_url='login')
def lecturer_panel(request):
    return render(request, 'home/lecturer-panel.html')



def lecturer_report(request):
    return render(request, 'home/lecturer-report.html')



def lecturer_summary(request):
    return render(request, 'home/lecturer-summary.html')



def manage_class(request):
    return render(request, 'home/manage-class.html')



def modify_class(request):
    return render(request, 'home/modify-class.html')



def modify_profile(request):
    return render(request, 'home/modify-profile.html')



def profile(request):
    return render(request, 'home/profile.html')






def student_summary(request):
    return render(request, 'home/student-summary.html')



def student_report(request):
    return render(request, 'home/student-report.html')



def student_modify(request):
    return render(request, 'home/student-modify.html')



def student_profile(request):
    return render(request, 'home/student-profile.html')


@login_required(login_url='login')
def student_panel(request):
    return render(request, 'home/student-panel.html')




























from .forms import LecturerRegistrationForm


@login_required(login_url='login')
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