from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models
from django.utils import timezone

# ================== Custom User Manager ==================
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with admin privileges"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True or extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_staff=True and is_superuser=True')
        return self.create_user(email, password, **extra_fields)

# ================== Custom User Model ==================
class CustomUser(AbstractUser):
    USER_ROLES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
    )
    username = None  # Remove username field
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=USER_ROLES)
    
    # Fix related_name conflicts
    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']

    def __str__(self):
        return self.email

# ================== Lecturer Model ==================
class Lecturer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    lecturer_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    profile_picture = models.ImageField(upload_to='lecturer_profiles/', blank=True, null=True)

    def __str__(self):
        return self.full_name

# ================== Academic Session & Semester ==================
class AcademicSession(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Semester(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# ================== Department ==================
class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# ================== Course ==================
class Course(models.Model):
    course_code = models.CharField(max_length=20)
    course_title = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    level = models.IntegerField(choices=[
        (100, '100 Level'),
        (200, '200 Level'),
        (300, '300 Level'),
        (400, '400 Level'),
    ])
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    attendance_day = models.CharField(max_length=10)
    attendance_start_time = models.TimeField()
    attendance_end_time = models.TimeField()

    def __str__(self):
        return f"{self.course_code} - {self.course_title}"

# ================== Student Model ==================
class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    matric_number = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    session = models.ForeignKey(AcademicSession, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    level = models.IntegerField(choices=[
        (100, '100 Level'),
        (200, '200 Level'),
        (300, '300 Level'),
        (400, '400 Level'),
    ])
    profile_picture = models.ImageField(upload_to='student_profiles/', blank=True, null=True)
    fingerprint_data = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.full_name} ({self.matric_number})"

# ================== Attendance Model ==================
class Attendance(models.Model):
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.student.full_name} - {self.course.course_code} - {self.status}"

    @staticmethod
    def is_within_timeframe(course):
        """Checks if the current time is within the allowed timeframe for attendance"""
        now = timezone.now().time()
        return course.attendance_start_time <= now <= course.attendance_end_time
