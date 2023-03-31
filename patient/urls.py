from django.urls import path
from . import views
app_name='patient'


urlpatterns=[
    path('index',views.patient_index,name='index'),
    path('doc_booking',views.patient_doc_booking,name='booking'),
    path('profile',views.patient_profile,name='profile'),
    path('booked',views.patient_booked,name='booked'),
    path('view_booking',views.patient_view_booking,name='view_booking'),
    path('pat_doctors',views.patient_pat_doctors,name='pat_doctors'),

    path('doctor_search',views.doctorSearchAjax,name='doctor_search'),
    path('searchdoctor',views.searchdoctor,name='searchdoctor'),


    path('view_search_result/<int:d_id>/',views.patient_view_search_result,name='search_result'),
   



    path('consultation_details/<int:consultation_id>/', views.patient_consultation_details, name='consultation_details'),
    path('change_password',views.patient_change_password,name='change_password'),
  
    path('view_prescription/<int:booking_id>/',views.patient_view_prescription,name='view_prescription'),

    path('logout',views.logout,name='logout'),
]