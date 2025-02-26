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

# Append static URLs if in DEBUG mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns = [
    path('', views.index, name='index'), 
    # path('login/', views.login, name='login'),
    path('login/', views.login_view, name='login'),
    path('admin_dashboard/', login_required(lambda request: render(request, 'home/admin_dashboard.html')), name='admin_dashboard'),
    path('student_panel/', login_required(lambda request: render(request, 'home/student-panel.html')), name='student_panel'),
    path('lecturer_panel/', login_required(lambda request: render(request, 'home/lecturer-panel.html')), name='lecturer_panel'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),






    path('mark/', views.mark, name='mark'),
    path('report/', login_required(views.report), name='report'),
    path('settings/', login_required(views.settings), name='settings'),
    path('course/', login_required(views.course), name='course'),
    path('admin_summary/', login_required(views.admin_summary), name='admin_summary'),
    path('add_student/', login_required(views.add_student), name='add_student'),
    path('add_lecturer/', login_required(views.add_lecturer), name='add_lecturer'),
    path('modify_lecturer/', login_required(views.modify_lecturer), name='modify_lecturer'),
    path('modify_lecturer_page/', login_required(views.modify_lecturer_page), name='modify_lecturer_page'),
    path('modify_course/', login_required(views.modify_course), name='modify_course'),
    path('modify_course_page/', login_required(views.modify_course_page), name='modify_course_page'),
    path('modify_student/', login_required(views.modify_student), name='modify_student'),
    path('modify_student_page/', login_required(views.modify_student_page), name='modify_student_page'),
    path('lecturer_report/', login_required(views.lecturer_report), name='lecturer_report'),
    path('lecturer_summary/', login_required(views.lecturer_summary), name='lecturer_summary'),
    path('profile/', login_required(views.profile), name='profile'),
    path('manage_class/', login_required(views.manage_class), name='manage_class'),
    path('modify_class/', login_required(views.modify_class), name='modify_class'),
    path('modify_profile/', login_required(views.modify_profile), name='modify_profile'),
    path('student_report/', login_required(views.student_report), name='student_report'),
    path('student_summary/', login_required(views.student_summary), name='student_summary'),
    path('student_modify/', login_required(views.student_modify), name='student_modify'),
    path('student_profile/', login_required(views.student_profile), name='student_profile'),
]
