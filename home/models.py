from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models
from django.utils import timezone
from django.conf import settings


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

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    username = None  # Remove username field
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=USER_ROLES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    
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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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


# ================== Student Model ==================
class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]

    
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    matric_number = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
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
    gender = models.CharField(
        max_length=1, 
        choices=GENDER_CHOICES,
        default='M' 
    )

    def __str__(self):
        return f"{self.full_name} ({self.matric_number})"
    
    def get_gender_display(self):
        """Override the default get_gender_display to ensure correct output"""
        return 'Male' if self.gender == 'M' else 'Female'


# ================== Course ==================
class Course(models.Model):
    course_code = models.CharField(max_length=20)
    course_title = models.CharField(max_length=100)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    level = models.IntegerField(choices=[
        (100, '100 Level'),
        (200, '200 Level'),
        (300, '300 Level'),
        (400, '400 Level'),
    ])

    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, related_name='courses')
    attendance_day = models.CharField(max_length=10)
    attendance_start_time = models.TimeField()
    attendance_end_time = models.TimeField()
    departments = models.ManyToManyField(Department, related_name='courses')
    is_general = models.BooleanField(default=False)

    def get_enrolled_students_count(self):
        return self.students.count()

    def get_attendance_count(self):
        return Attendance.objects.filter(course=self).count()

    @classmethod
    def get_lecturer_stats(cls, lecturer):
        """Get all stats for a lecturer in one query"""
        courses = cls.objects.filter(lecturer=lecturer)
        total_courses = courses.count()
        
        # Get students directly from course relationships
        total_students = Student.objects.filter(
            courses__lecturer=lecturer
        ).distinct().count()
        
        # Get attendance count
        total_attendance = Attendance.objects.filter(
            course__lecturer=lecturer
        ).count()
        
        return {
            'total_courses': total_courses,
            'total_students': total_students,
            'total_attendance': total_attendance
        }
    
    def delete(self, *args, **kwargs):
        try:
            # First delete all related attendance records
            self.attendances.all().delete()
            # Then delete the course itself
            super().delete(*args, **kwargs)
            return True
        except Exception as e:
            print(f"Error deleting course: {str(e)}")
            return False

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Check if this is a new course
        super().save(*args, **kwargs)
        
        if is_new:
            # This will trigger after the course is saved
            if self.is_general:
                # Add all departments if it's a general course
                self.departments.set(Department.objects.all())
            # For non-general courses, departments are handled by the form


# ================== Attendance Model ==================
class Attendance(models.Model):
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE,
        related_name='attendances',
        db_constraint=True  # Enforces database-level constraint
    )
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        # Add indexes and constraints
        indexes = [
            models.Index(fields=['course', 'student', 'date']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'course', 'date'], 
                name='unique_attendance'
            )
        ]

    def __str__(self):
        return f"{self.student.full_name} - {self.course.course_code} - {self.status}"

    @staticmethod
    def is_within_timeframe(course):
        """Checks if the current time is within the allowed timeframe for attendance"""
        now = timezone.now().time()
        return course.attendance_start_time <= now <= course.attendance_end_time
    

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Course)
def assign_course_to_students(sender, instance, created, **kwargs):
    """Automatically assign course to students based on departments and level"""
    if created:  # Only run when a new course is created
        # Get all departments for this course
        if instance.is_general:
            departments = Department.objects.all()
        else:
            departments = instance.departments.all()

        # Get all students in the selected departments and level
        students = Student.objects.filter(
            department__in=departments,
            level=instance.level
        )

        # Add course to each student
        instance.students.add(*students)