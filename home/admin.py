from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, Lecturer, AcademicSession, Semester, 
    Department, Course, Student, Attendance
)

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'role', 'is_staff', 'is_active')
    search_fields = ('email', 'role')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Role', {'fields': ('role',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'is_active', 'is_staff')}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)

# Custom Lecturer Admin
class LecturerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'lecturer_id', 'phone', 'user_email', 'profile_picture')
    search_fields = ('full_name', 'lecturer_id', 'phone')
    
    def user_email(self, obj):
        return obj.user.email
    user_email.admin_order_field = 'user__email'
    user_email.short_description = 'Email'

admin.site.register(Lecturer, LecturerAdmin)

# Student Admin
class StudentAdmin(admin.ModelAdmin):
    list_display = ('matric_number', 'full_name', 'gender', 'department', 'level', 'session')
    list_filter = ('gender', 'department', 'level', 'session')
    search_fields = ('matric_number', 'full_name')
    ordering = ('matric_number',)
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.admin_order_field = 'user__first_name'
    get_full_name.short_description = 'Full Name'

    def user_email(self, obj):
        return obj.user.email
    user_email.admin_order_field = 'user__email'
    user_email.short_description = 'Email'

admin.site.register(Student, StudentAdmin)

# Attendance Admin
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'matric_number', 'course_code', 'course_title', 
                   'lecturer_name', 'date', 'timestamp', 'status', 'semester', 'session')
    list_filter = ('status', 'date', 'course', 'semester', 'session')
    search_fields = ('student__matric_number', 'student__full_name', 
                    'course__course_code', 'course__course_title')
    date_hierarchy = 'date'
    ordering = ('-date', '-timestamp')

    def student_name(self, obj):
        return obj.student.full_name
    student_name.admin_order_field = 'student__full_name'
    student_name.short_description = 'Student Name'

    def matric_number(self, obj):
        return obj.student.matric_number
    matric_number.admin_order_field = 'student__matric_number'
    matric_number.short_description = 'Matric Number'

    def course_code(self, obj):
        return obj.course.course_code
    course_code.admin_order_field = 'course__course_code'
    course_code.short_description = 'Course Code'

    def course_title(self, obj):
        return obj.course.course_title
    course_title.admin_order_field = 'course__course_title'
    course_title.short_description = 'Course Title'

    def lecturer_name(self, obj):
        return obj.course.lecturer.full_name
    lecturer_name.admin_order_field = 'course__lecturer__full_name'
    lecturer_name.short_description = 'Lecturer'

    readonly_fields = ('date', 'timestamp')
    
    fieldsets = (
        ('Student Information', {
            'fields': ('student',)
        }),
        ('Course Information', {
            'fields': ('course', 'semester', 'session')
        }),
        ('Attendance Details', {
            'fields': ('status', 'date', 'timestamp')
        }),
    )

admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(AcademicSession)
admin.site.register(Semester)
admin.site.register(Department)
admin.site.register(Course)
