from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Lecturer, AcademicSession, Semester, Department, Course

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'role', 'is_staff', 'is_active')
    search_fields = ('email', 'role')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),  # Removed full_name
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
    user_email.admin_order_field = 'user__email'  # Allows sorting by user email
    user_email.short_description = 'Email'  # Set column name in admin view

admin.site.register(Lecturer, LecturerAdmin)

# Register other models if necessary
admin.site.register(AcademicSession)
admin.site.register(Semester)
admin.site.register(Department)
admin.site.register(Course)



from django.contrib import admin
from .models import Student

class StudentAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'matric_number', 'user_email', 'department', 'session', 'level')
    search_fields = ('matric_number', 'user__email', 'user__first_name', 'user__last_name')
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.admin_order_field = 'user__first_name'
    get_full_name.short_description = 'Full Name'

    def user_email(self, obj):
        return obj.user.email
    user_email.admin_order_field = 'user__email'
    user_email.short_description = 'Email'

admin.site.register(Student, StudentAdmin)
