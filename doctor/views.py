from audioop import reverse
from multiprocessing import context
from pyexpat.errors import messages
from django.forms import ValidationError
from django.shortcuts import redirect, render
from admin_app.models import Consultation
from common_app.models import Departments, Doctors, Patient
from doctor.decorators import auth_doctor
from doctor.models import Prescription
from django.http import HttpResponse, JsonResponse
from patient.models import Booking
from django.contrib import messages

# Create your views here.
@auth_doctor
def doctor_base(request):
    
    return render(request,'doctor_templates/base.html')


@auth_doctor
def doctor_index(request):
    doctor = Doctors.objects.filter(id = request.session['doctor']).values('doctor_name','doctor_image')
    print(doctor)
    doctor_name = doctor[0]['doctor_name']
    doctor_pic = doctor[0]['doctor_image']




    doctor = Doctors.objects.get(id = request.session['doctor'])
    total_patients = Booking.objects.filter(doctor_name=doctor).count()
    consulted = Booking.objects.filter(doctor_name=doctor, status='consulted').count()
    booked = Booking.objects.filter(doctor_name=doctor, status='booked').count()



    appointments = Booking.objects.filter(doctor_name=doctor, status='booked' ).order_by('-booking_date')[0:5]
    recent_appointments = {}
    for appoint in appointments:
        if appoint.patient_email in recent_appointments:
            if appoint.booking_date > recent_appointments[appoint.patient_email].booking_date:

                recent_appointments[appoint.patient_email] = appoint
        else:
            recent_appointments[appoint.patient_email] = appoint
    recent_appointments_list = list(recent_appointments.values())

    context = {
        'd_name': doctor_name,
        'd_image': doctor_pic,
        'total_patients':total_patients,
        'recent_apponitments': recent_appointments_list,
        'consulted':consulted,
        'booked':booked
    }

    return render(request,'doctor_templates/index.html',context)


@auth_doctor
def doctor_patient_page(request):
    return render(request,'doctor_templates/patient_page.html',)

@auth_doctor
def doctor_patient_booked(request):
    doctor = Doctors.objects.get(id = request.session['doctor'])
    booked_patients = Booking.objects.filter(doctor_name = doctor, status = 'booked')
    return render(request,'doctor_templates/patient_booked.html',{'booked_patients':booked_patients})



@auth_doctor
def doctor_patient_record(request):
    doctor = Doctors.objects.get(id = request.session['doctor'])
    
    patient_record = Booking.objects.filter(doctor_name = doctor, status = 'consulted')
    
    return render(request,'doctor_templates/patient_record.html',{'patients':patient_record})



@auth_doctor   
def doctor_view_prescription(request,booking_id):
    booked_patient = Booking.objects.get(id=booking_id)
    
    prescript = Prescription.objects.filter(booking_id=booking_id)
    return render(request,'doctor_templates/view_prescription.html',{'pre':prescript,'book':booked_patient})


@auth_doctor
def doctor_change_password(request):
    error_msg = ''
    success_msg = ''

    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        if new_password == confirm_password:
            if len(new_password) >= 8:
                doctor = Doctors.objects.get(id = request.session['doctor'])
                if doctor.password == old_password:

                    doctor.password = new_password
                    doctor.save()
                    success_msg = 'Password changed successfully'
                else:
                    error_msg = 'Incorrect Password'
            else:
                error_msg = 'Password should be 8 charecters long'
            
        else:
            error_msg = 'Password doesn\'t match'
    
    return render(request,'doctor_templates/change_password.html',{'error_message' : error_msg, 'success_message': success_msg})


@auth_doctor
def doctor_doctor_profile(request):
    profile = Doctors.objects.filter(id = request.session['doctor'])
   

    if request.method == 'POST':
        
        new_name = request.POST['name']
        new_phone = request.POST['phone']
        new_address = request.POST['address']
        new_email = request.POST['email']
        new_gender = request.POST['pat_gender']
        new_department_id = int(request.POST['department'])
        new_department = Departments.objects.get(id=new_department_id)
        
        doctor = Doctors.objects.get(id = request.session['doctor'])#.update(patient_name = new_name,patient_mobile = new_phone, patient_address = new_address, patient_email = new_email)
        doctor.doctor_name = new_name
        doctor.doctor_phone  = new_phone
        doctor.doctor_address  = new_address
        doctor.doctor_address  = new_email
        doctor.doctor_department = new_department 
        doctor.doctor_gender = new_gender
    

        doctor.save()
        msg = "Update Successfully!"
    new_department = Departments.objects.all()
    return render(request,'doctor_templates/doctor_profile.html',{'profile':profile, 'departments':new_department})


def doctor_delete_appointment(request):
   doctor = Doctors.objects.get(id = request.session['doctor'])
   appointment = Booking.objects.filter(doctor_name = doctor,status = 'booked')
   return render(request,'doctor_templates/delete_appointment.html',{'appointments':appointment})
def remove_appointment(request,d_id):
    app_list = Booking.objects.get(id = d_id)
    app_list.delete()
    return redirect('doctor:delete_appointment')


@auth_doctor
def doctor_appointments(request):
    return render(request,'doctor_templates/appointments.html')

@auth_doctor
def doctor_view_appointment(request):
    doctor = Doctors.objects.get(id = request.session['doctor'])
    appointment = Booking.objects.filter(doctor_name = doctor,status = 'booked')
    return render(request, 'doctor_templates/view_appointment.html', {'appointments':appointment})



@auth_doctor
def add_prescription(request,b_id):
    
    doctor = Doctors.objects.get(id = request.session['doctor'])
    return redirect('doctor:prescription')



@auth_doctor
def doctor_prescription(request, booking_id):
    msg = ''
    bkng = Booking.objects.get(id=booking_id)
    
    
    if request.method == 'POST':
        print('test.............................')
        
        pdiagnosis = request.POST['p_diagnosis']
        pname = request.POST['p_name']
        ppurpose = request.POST['p_purpose']
        pdosage = request.POST['p_dosage']
        proute = request.POST['p_route']
        pfrequency = request.POST['p_frequency']
        prescription = Prescription(booking=bkng, diagnosis=pdiagnosis, medication_name=pname, purpose=ppurpose, dosage=pdosage, route=proute, frequency=pfrequency)
        prescription.status = 'consulted'
        
        prescription.save()
        bkng.status = 'consulted'
        bkng.save()
        msg = 'Prescription added successfully'
        
        
    prescription_list = Prescription.objects.filter(booking=bkng)
    print(prescription_list)
    return render(request, 'doctor_templates/prescription.html', {'message1': msg, 'list': prescription_list, 'booking': bkng})

def delete_item(request,booking_id):
    item = Prescription.objects.get(id = booking_id)
    item.delete()
    messages.success(request, 'One prescription removed')
    return redirect('doctor:prescription', booking_id=item.booking_id)

def edit_item(request,booking_id):
    ed_item = Prescription.objects.get(id = booking_id)
    bkng = Booking.objects.get(id=ed_item.booking.id)
    prescription_list = Prescription.objects.filter(booking=bkng)
    context = {
        'ed_item':ed_item,
        'prescription_list':prescription_list
    }
    
    return render(request,'doctor_templates/prescription.html',context)


def update_item(request,booking_id):
    if request.method == 'POST':

        item = Prescription.objects.get(id = booking_id)
        item.diagnosis = request.POST['p_diagnosis']
        item.medication_name = request.POST['p_name']
        item.purpose = request.POST['p_purpose']
        item.dosage = request.POST['p_dosage']
        item.route = request.POST['p_route']
        item.frequency = request.POST['p_frequency']
        item.save()
        messages.success(request, 'prescription Updated Successfully')
        
        
    return redirect('doctor:prescription', booking_id=item.booking_id)

@auth_doctor
def doctor_consultation(request):
    
    consultation_detail = Consultation.objects.filter(doctor_id = request.session['doctor'])

    
    return render(request,'doctor_templates/consultation.html',{'consultation_details':consultation_detail})

def update_consultation_status(request):
    if request.method == 'POST':
        consultation_id = request.POST['consultation_id']
        new_status = request.POST['new_status']
        consultation = Consultation.objects.get(id=consultation_id)
        consultation.status = new_status
        consultation.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})



def doctor_logout(request):
    if 'doctor' in request.session:
        request.session.pop('doctor')
    return redirect('common_app:home')







