"""
URL configuration for hostel_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from hostel import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.landing, name='landing'),
    path('', views.home, name='home'),
    # path('export-students/', views.export_stud_csv, name='export_students'),
    path('rent/', views.rent, name='rent'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('logout/', views.student_logout, name='logout'),
    path('student_dashboard', views.student_dashboard, name='student_dashboard'),
    path('student_profile', views.student_profile, name='student_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('rent_status/', views.rent_status, name="rent_status"),
    path('room_info/', views.room_info, name='room_info'),
    path('complaint/', views.complaint, name="complaint"),
    path('complaint_history/', views.complaint_history, name="complaint_history"),
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
    path('apply-leave/',views.apply_leave,name='apply_leave'),
    path('leave-history/',views.leave_history,name='leave_history'),
    path('student-login/',views.student_login,name='student_login'),
    path('hostel-login/',views.hostel_login,name='hostel_login'),
    path('hostel-dashboard/',views.hostel_dashboard,name='hostel_dashboard'),
    path('manage-leaves/',views.manage_leaves,name='manage_leaves'),
    path('manage-complaints/',views.manage_complaints,name='manage_complaints'),
    path('view-students/',views.view_students,name='view_students'),
    path('view-attendance/', views.view_attendance,name='view_attendance'),
    path('hostel-logout/',views.hostel_logout,name='hostel_logout'),
    # path('approve-leave/<int:leave_id>/',views.approve_leave,name='approve_leave'),
    # path('reject-leave/<int:leave_id>/',views.reject_leave,name='reject_leave'),
    path('resolve-complaint/<int:complaint_id>/',views.resolve_complaint,name='resolve_complaint'),
    path(
        'apply-outpass/',
        views.apply_outpass,
        name='apply_outpass'
    ),

    path(
        'outpass-history/',
        views.outpass_history,
        name='outpass_history'
    ),

    path(
        'view-outpass/<int:outpass_id>/',
        views.view_outpass,
        name='view_outpass'
    ),

    # Hostel Incharge
    path(
        'manage-outpasses/',
        views.manage_outpasses,
        name='manage_outpasses'
    ),

    path(
        'approve-outpass/<int:outpass_id>/',
        views.approve_outpass,
        name='approve_outpass'
    ),

    path(
        'reject-outpass/<int:outpass_id>/',
        views.reject_outpass,
        name='reject_outpass'
    ),

    # Security Verification
    path(
        'verify-outpass/<str:outpass_code>/',
        views.verify_outpass,
        name='verify_outpass'
    ),
    path(
    'leave-management/',
    views.leave_management,
    name='leave_management'
),
    path(
    'view-leave/<int:leave_id>/',
    views.view_leave,
    name='view_leave'
),
    path('holiday-list/',views.holiday_list, name='holiday_list'),
    path('incharge/holidays/', views.holiday_list, name='holiday_list'),
    path('incharge/holidays/add/', views.holiday_create, name='holiday_create'),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )