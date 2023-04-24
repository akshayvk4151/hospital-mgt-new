from django.urls import path
from . import views
app_name='admin_app'


urlpatterns=[

    path('index',views.admin_app_index,name='index'),
    path('view_messages',views.admin_app_view_messages,name='view_messages'),
    path('clear_all', views.clear_all, name='clear_all'),

    path('doctor_page',views.admin_app_doctor_page,name='doctor_page'),
    path('adm_departments',views.admin_app_adm_departments,name='adm_departments'),
    path('department/remove/<int:d_id>',views.remove_department,name='remove_department'),
    path('add_department',views.admin_app_add_department,name='add_departments'),
    path('change_department/<int:e_id>',views.admin_app_change_department,name='change_departments'),
    path('approve_doctor',views.admin_app_approve_doctor,name='approve_doctor'),
    path('doctor_specialisation',views.admin_app_doctor_specialisation,name='doctor_specialisation'),
    path('doctor_record',views.admin_app_doctor_record,name='doctor_record'),
    path('doctor/remove/<int:d_id>',views.remove_doctor_record,name='remove_doctor'),
    path('register_doctor',views.admin_app_register_doctor,name='register_doctor'),
    path('checkemail_admin',views.check_email_doctor,name='check_email_doctor'),

    path('consultation/<int:d_id>',views.admin_app_consultation,name='consultation'),
    path('check_day/', views.check_day, name='check_day'),
    path('delete_consultation/<int:c_id>/', views.delete_consultation, name='delete_consultation'),
    path('edit_consultation/<int:d_id>/', views.edit_consultation, name='edit_consultation'),
    path('update_consultation/<int:d_id>/',views.update_consultation,name='update_consultation'),
    



    path('patient_page',views.admin_app_patient_page,name='patient_page'),
    path('patient_registered',views.admin_app_patient_registered,name='patient_registered'),
    path('patient_registered/remove/<int:d_id>',views.remove_regpatient_record,name='remove_patient'), 
    path('approve_patient',views.admin_app_approve_patient,name='approve_patient'),
    path('view_patients',views.admin_app_view_patients,name='view_patients'),
    path('consulted_patient',views.admin_app_consulted_patient,name='consulted_patient'),
    path('consulted_patient/remove/<int:p_id>',views.remove_consulted_patient,name='remove_consulted_patient'),
    path('patient_record/remove/<int:p_id>',views.remove_patient_record,name='remove_patient'),
    path('book_patient',views.admin_app_book_patient,name='book_patient'),


    path('appointments',views.admin_app_appointments,name='appointments'),
    path('admin_logout',views.admin_logout,name='admin_logout'),
    
  
]