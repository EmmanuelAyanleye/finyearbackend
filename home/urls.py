from django.shortcuts import render
from django.urls import path
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import login_view


from django.conf import settings
from django.conf.urls.static import static
from .views import add_lecturer

from django.contrib.auth.decorators import login_required


# Define urlpatterns before using it
urlpatterns = [
    path('add_lecturer/', add_lecturer, name='add_lecturer'),
]

from django.urls import path
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect


# Append static URLs if in DEBUG mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

def is_lecturer(user):
    return user.is_authenticated and user.role == 'lecturer'

def is_student(user):
    return user.is_authenticated and user.role == 'student'

admin_dashboard_view = login_required(user_passes_test(is_admin, login_url='index')(lambda request: render(request, 'home/admin_dashboard.html')))
student_panel_view = login_required(user_passes_test(is_student, login_url='index')(lambda request: render(request, 'home/student-panel.html')))
lecturer_panel_view = login_required(user_passes_test(is_lecturer, login_url='index')(lambda request: render(request, 'home/lecturer-panel.html')))


urlpatterns = [
    path('', views.index, name='index'), 
    # path('login/', views.login, name='login'),
    path('login/', views.login_view, name='login'),
    path('admin_dashboard/', admin_dashboard_view, name='admin_dashboard'),
    path('student_panel/', student_panel_view, name='student_panel'),
    path('lecturer_panel/', lecturer_panel_view, name='lecturer_panel'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
    path('get_attendance_data/', views.get_attendance_data, name='get_attendance_data'),
    path('export_excel/', views.export_excel, name='export_excel'),
    path('get_attendance_summary/', views.get_attendance_summary, name='get_attendance_summary'),
    path('export_summary_pdf/', views.export_summary_pdf, name='export_summary_pdf'),
    path('get-dashboard-stats/', views.get_dashboard_stats, name='get_dashboard_stats'),


    path('fingerprint/', views.fingerprint, name='fingerprint'),
    path('verify/', views.verify, name='verify'),
    path('mark/', views.mark, name='mark'),
    path('get-courses/', views.get_courses, name='get_courses'),
    path('report/', views.report, name='report'),
    path('settings/', views.settings, name='settings'),
    path('course/', views.course, name='course'),
    path('admin_summary/', views.admin_summary, name='admin_summary'),
    path('add_student/', views.add_student, name='add_student'),
    path('add_lecturer/', views.add_lecturer, name='add_lecturer'),
    path('modify_lecturer/', views.modify_lecturer, name='modify_lecturer'),
    
    path('delete_lecturer/<int:lecturer_id>/', views.delete_lecturer, name='delete_lecturer'),
    path('modify_lecturer_page/<str:lecturer_id>/', views.modify_lecturer_page, name='modify_lecturer_page'),

    path('modify_course/', views.modify_course, name='modify_course'),
    path('delete_course/<int:course_id>/', views.delete_course, name='delete_course'),
    path('modify_course_page/<int:course_id>/', views.modify_course_page, name='modify_course_page'),
    path('modify_student/', views.modify_student, name='modify_student'),
    path('delete_student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('modify_student_page/<int:student_id>/', views.modify_student_page, name='modify_student_page'),

    path('lecturer_report/', views.lecturer_report, name='lecturer_report'),
    path('get_lecturer_attendance_data/', views.get_lecturer_attendance_data, name='get_lecturer_attendance_data'),
    path('export_lecturer_attendance/', views.export_lecturer_attendance, name='export_lecturer_attendance'),
    
    path('lecturer_summary/', views.lecturer_summary, name='lecturer_summary'),
    path('get_lecturer_summary_data/', views.get_lecturer_summary_data, name='get_lecturer_summary_data'),
    path('export_summary_pdf/', views.export_summary_pdf, name='export_summary_pdf'),
    path('profile/', views.profile, name='profile'),
    path('manage_class/', views.manage_class, name='manage_class'),
    path('modify_class/<int:course_id>/', views.modify_class, name='modify_class'),
    path('modify_profile/', views.modify_profile, name='modify_profile'),
    path('student_report/', views.student_report, name='student_report'),
    path('student_summary/', views.student_summary, name='student_summary'),
    path('student_modify/', views.student_modify, name='student_modify'),
    path('student_profile/', views.student_profile, name='student_profile'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)