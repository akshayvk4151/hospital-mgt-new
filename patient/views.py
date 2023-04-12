from random import randint
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from admin_app.models import Consultation
from common_app.models import Doctors, Patient
from doctor.models import Prescription
from patient.decorators import auth_patient
from django.http import Http404

from patient.models import Booking
# Create your views here.






@auth_patient
def patient_index(request):
    pat = Patient.objects.filter(id = request.session['patient']).values('patient_name')
    print(pat)
    patient_name = pat[0]['patient_name']
    


    patient_id = request.session['patient']
    booking_view = Booking.objects.filter(patient_id=patient_id).order_by('-id')[0:1]
    
    recent_booking = {}
    for book in booking_view:
        if book.patient_email in recent_booking:
            if book.booking_date > recent_booking[book.patient_email].booking_date:
                recent_booking[book.patient_email] = book
        else:
            recent_booking[book.patient_email] = book
    recent_booking_list = list(recent_booking.values())

    doctor = None
    if recent_booking_list:
        recent_booking = recent_booking_list[0]
        try:
            doctor = Doctors.objects.get(id=recent_booking.doctor_name.id)
        except Doctors.DoesNotExist:
            pass
    print(doctor,'00000000000')
    return render(request,'patient_templates/index.html',{'booking_list':recent_booking_list ,'doctor': doctor,'p_name':patient_name})

@auth_patient
def patient_doc_booking(request):
    
    doctor = None
   
    if request.method == 'POST':
        pname = request.POST['pat_name']
        pemail = request.POST['pat_email']
        pphone = request.POST['pat_phone']
        pgender = request.POST['pat_gender']
        pbirth = request.POST['pat_birth']
        page = request.POST['pat_age']
        pdate = request.POST['pat_date']
        ptime = request.POST['pat_time']
        pdoctor = request.POST['pat_doctor']
        pdescription = request.POST['pat_description']
        paddress = request.POST['pat_address']
        ref_no = 'REF-'+ str(randint(1000,9999))+ pphone[6:]
        doctor = Doctors.objects.get(id=pdoctor)
        
        booking = Booking(patient_name = pname,
                        patient_email = pemail,
                        patient_phone = pphone,
                        patient_gender = pgender,
                        birth_date =pbirth ,
                        patient_age = page, 
                        booking_date = pdate, 
                        booking_time = ptime, doctor_name = doctor, 
                        patient_description = pdescription,
                        patient_address = paddress,
                        reference_no = ref_no,
                        patient_id=request.session['patient'])
        booking.save()
        booking_id = booking.id  # get the ID of the newly created booking
        request.session['booking_id'] = booking_id 
        return redirect("patient:booked")
        

    else:
        doctors = Doctors.objects.filter(status = 'approved') 
        

    
        

    return render(request,'patient_templates/doc_booking.html',{'doctor':doctors} )

@auth_patient
def patient_profile(request):
    msg = ''
    profile = Patient.objects.filter(id = request.session['patient'])
    
    if request.method == 'POST':
        
        new_name = request.POST['name']
        new_phone = request.POST['phone']
        new_address = request.POST['address']
        new_email = request.POST['email']
        patient = Patient.objects.get(id = request.session['patient'])#.update(patient_name = new_name,patient_mobile = new_phone, patient_address = new_address, patient_email = new_email)
        patient.patient_name = new_name
        patient.patient_mobile = new_phone
        patient.patient_address = new_address
        patient.patient_email = new_email

        patient.save()
        msg = "Update Successfully!"


    return render(request,'patient_templates/profile.html',{'profile':profile,'message':msg})
@auth_patient
def patient_booked(request):
    return render(request,'patient_templates/booked.html')


@auth_patient
def patient_your_bookings(request):
    return render(request,'patient_templates/your_bookings.html')
    
@auth_patient
def patient_prescription_list(request):
    patient_id = request.session['patient']
    patient_view = Booking.objects.filter(patient_id=patient_id, status = 'consulted')
    # patient_view = Booking.objects.filter(id = request.session['patient'])
    print(patient_view)
    return render(request,'patient_templates/prescription_list.html',{'views':patient_view})

@auth_patient
def patient_view_bookings(request):
    patient_id = request.session['patient']
    patient_view = Booking.objects.filter(patient_id=patient_id, status__in=['pending', 'booked'])
    # patient_view = Booking.objects.filter(id = request.session['patient'])
    print(patient_view)
    return render(request,'patient_templates/view_bookings.html',{'views':patient_view})

@auth_patient
def patient_pat_doctors(request):
    doctor = Doctors.objects.filter(status = 'approved')
    return render(request,'patient_templates/pat_doctors.html',{'doctor':doctor})

def doctorSearchAjax(request):
    doctors = Doctors.objects.filter(status = 'approved').values_list('doctor_name', flat=True)
    doctorList = list(doctors)

    return JsonResponse(doctorList, safe=False)

def searchdoctor(request):
    if request.method == 'POST':
        searchedterm = request.POST.get('doctorsearch')
        if searchedterm == "":
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            doct = Doctors.objects.filter(doctor_name = searchedterm).first()

            if doct:
                return redirect(f'/patient/view_search_result/{doct.id}/') # f formatted string
    return redirect(request.META.get('HTTP_REFERER'))

@auth_patient
def patient_view_search_result(request, d_id):
    doctor = Doctors.objects.get(id=d_id)
    return render(request,'patient_templates/view_search_result.html',{'doc':doctor})



@auth_patient
def patient_consultation_details(request, consultation_id):

    consultation = Consultation.objects.filter(doctor_id=consultation_id).order_by('id')
    doctor = Doctors.objects.filter(id = consultation_id).values('doctor_name')[0]['doctor_name']
    print(doctor)
    return render(request, 'patient_templates/consultation_details.html', {'details': consultation,'doctor_name':doctor})

@auth_patient
def patient_change_password(request):
    error_msg = ''
    success_msg = ''

    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        if new_password == confirm_password:
            if len(new_password) >= 8:
                patient = Patient.objects.get(id = request.session['patient'])
                if patient.patient_password == old_password:

                    patient.patient_password = new_password
                    patient.save()
                    success_msg = 'Password changed successfully'
                else:
                    error_msg = 'Incorrect Password'
            else:
                error_msg = 'Password should be 8 charecters long'
            
        else:
            error_msg = 'Password doesn\'t match'
    
    return render(request,'patient_templates/change_password.html',{'error_message' : error_msg, 'success_message': success_msg})



@auth_patient
def patient_view_prescription(request,booking_id):
    booked_patient = Booking.objects.get(id=booking_id)
    
    prescript = Prescription.objects.filter(booking_id=booking_id)
    return render(request,'patient_templates/view_prescription.html',{'pre':prescript,'book':booked_patient})




def patient_logout(request):
    if 'patient' in request.session:
        request.session.pop('patient')
    return redirect('common_app:home')

