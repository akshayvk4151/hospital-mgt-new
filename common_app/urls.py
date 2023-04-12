from django.urls import path
from . import views
app_name='common_app'


urlpatterns=[
    path('',views.common_app_index,name='home'),
   
    path('about',views.common_app_about,name='about'),
    path('contact',views.common_app_contact,name='contact'),
    path('patient_click',views.common_app_patient_click,name='patient_click'),
    path('patient_login',views.common_app_patient_login,name='patient_login'),
    path('patient_register',views.common_app_patient_register,name='patient_register'),
    path('doctors_login',views.common_app_doctors_login,name='doctors_login'),
    path('doctors_register',views.common_app_doctors_register,name='doctor_register'),
    path('doc_logincheck/<int:doctor_id>/',views.common_app_doc_logincheck, name='doc_logincheck'),



    path('department',views.common_app_department,name='department'),
    path('doctors',views.common_app_doctors,name='doctors'),
    path('doctor_click',views.common_app_doctor_click,name='doctor_click'),
    path('admin_click',views.common_app_admin_click,name='admin_click'),
    path('admin_register',views.common_app_admin_register,name='admin_register'),
    path('admin_login',views.common_app_admin_login,name='admin_login'),
    
    path('checkemail',views.check_email,name='check_email'),
    path('checkemail_doctor',views.check_email_admin,name='check_email_admin'),
    path('checkemail_admin',views.check_email_doctor,name='check_email_doctor'),

    
]