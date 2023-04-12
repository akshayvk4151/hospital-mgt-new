from django.urls import path
from . import views
app_name='doctor'


urlpatterns=[
    path('base',views.doctor_base,name='base'),
    path('index',views.doctor_index,name='index'),


    path('appointments',views.doctor_appointments,name='appointments'),
   
    path('delete_appointment',views.doctor_delete_appointment,name='delete_appointment'),
    path('remove_appointment/<int:d_id>',views.remove_appointment,name='remove_app'),

    path('patient_page',views.doctor_patient_page,name='patient_page'),
    path('patient_record',views.doctor_patient_record,name='patient_record'),
    path('patient_booked',views.doctor_patient_booked,name='patient_booked'),
  
    path('view_prescription/<int:booking_id>',views.doctor_view_prescription,name='view_prescription'),

    path('change_password',views.doctor_change_password,name='change_password'),
    path('doctor_profile',views.doctor_doctor_profile,name='doctor_profile'),

    path('view_appointment/', views.doctor_view_appointment, name='view_appointment'),
    path('add_prescription/<int:b_id>/',views.add_prescription,name='add_prescription'),
    path('doctor/prescription/<int:booking_id>/',views.doctor_prescription,name='prescription'),
    path('delete_item/<int:booking_id>/',views.delete_item,name='delete_item'),
    path('edit_item/<int:booking_id>/',views.edit_item,name='edit_item'),
    path('update_item/<int:booking_id>/',views.update_item,name='update_item'),
    path('consultation',views.doctor_consultation,name='consultation'),
    path('update_consultation_status',views.update_consultation_status,name='update_consultation_status'),



    path('doctor_logout',views.doctor_logout,name='doctor_logout'),
]