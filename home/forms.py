from django import forms
# home/forms.py
from django import forms
from .models import Lecturer
from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))



class LecturerRegistrationForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}))
    profile_picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Lecturer
        fields = ['lecturer_id', 'full_name', 'email', 'password', 'phone', 'profile_picture']

        widgets = {
            'lecturer_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter lecturer ID'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
        }



from django import forms
from django.contrib.auth import get_user_model
from .models import Lecturer

User = get_user_model()

class LecturerProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    
    class Meta:
        model = Lecturer
        fields = ['full_name', 'phone', 'profile_picture']
    
    def save(self, user, commit=True):
        lecturer = super().save(commit=False)

        # Check if the email is being changed
        new_email = self.cleaned_data['email']
        if new_email and new_email != user.email:
            # Ensure the new email does not already exist in the database
            if User.objects.filter(email=new_email).exclude(id=user.id).exists():
                raise forms.ValidationError("This email is already in use by another account.")
            user.email = new_email  # Update the email only if it's not already in use
        
        # Update password if provided
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)

        if commit:
            user.save()
            lecturer.save()
        return lecturer







from django import forms
from .models import AcademicSession, Semester, Department

class AcademicSessionForm(forms.ModelForm):
    class Meta:
        model = AcademicSession
        fields = ['name']

class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['name']

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']


from .models import Course, Department, Semester, Lecturer

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_code', 'course_title', 'department', 'semester', 'level', 'lecturer', 'attendance_day', 'attendance_start_time', 'attendance_end_time']
        
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label="Select a department", widget=forms.Select(attrs={'class': 'form-select'}))
    semester = forms.ModelChoiceField(queryset=Semester.objects.all(), empty_label="Select a semester", widget=forms.Select(attrs={'class': 'form-select'}))
    lecturer = forms.ModelChoiceField(queryset=Lecturer.objects.all(), empty_label="Select a lecturer", widget=forms.Select(attrs={'class': 'form-select'}))
    attendance_day = forms.ChoiceField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday')], widget=forms.Select(attrs={'class': 'form-select'}))
    attendance_start_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}))
    attendance_end_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}))



from .models import Student
class StudentForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,  # Allow the password field to be empty
    )

    class Meta:
        model = Student
        fields = ['full_name', 'matric_number', 'department', 'level', 'session', 'profile_picture']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'matric_number': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'level': forms.Select(attrs={'class': 'form-select'}),
            'session': forms.Select(attrs={'class': 'form-select'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }




class StudentSelfUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False  # Allow the password field to be empty
    )
    profile_picture = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Student
        fields = ['email', 'password', 'profile_picture']


class StudentUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password (leave empty to keep current)'
        }), 
        required=False
    )
    session = forms.ModelChoiceField(
        queryset=AcademicSession.objects.all().order_by('-name'),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    profile_picture = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
            'onchange': 'previewImage(this)'
        }),
        required=False
    )
    
    class Meta:
        model = Student
        fields = ['full_name', 'matric_number', 'gender', 'level', 
                 'session', 'department', 'profile_picture']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'matric_number': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'level': forms.Select(attrs={'class': 'form-select'}),
        }