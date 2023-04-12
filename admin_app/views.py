from random import randint
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy
from admin_app.decorators import auth_admin
from admin_app.models import Consultation

from common_app.models import Admin, Contact, Departments, Doctors, Patient
from patient.models import Booking
from django.contrib import messages


# Create your views here.

@auth_admin
def admin_app_index(request):
    admin = Admin.objects.filter(id = request.session['admin']).values('admin_name')
    
    admin_name = admin[0]['admin_name']
    doctor = Doctors.objects.all().count()   
    patient = Patient.objects.all().count() # customer count
    booking = Booking.objects.all().count()



    doctor_list = Doctors.objects.all().order_by('-id')[0:5]
    recent_doctors = {}
    for reg in doctor_list:
        if reg.doctor_email in recent_doctors:
            if reg.id > recent_doctors[reg.doctor_email].id:

                 recent_doctors[reg.doctor_email] = reg
        else:
            recent_doctors[reg.doctor_email] = reg
    reg_doctors_list = list(recent_doctors.values())


    patient_list = Patient.objects.all().order_by('-id')[0:10]
    recent_patients = {}
    for regs in patient_list:
        if regs.patient_email in recent_patients:
            if regs.id > recent_patients[regs.patient_email].id:

                 recent_patients[regs.patient_email] = regs
        else:
            recent_patients[regs.patient_email] = regs
    reg_patient_list = list(recent_patients.values())
    
    return render(request,'admin_app_templates/index.html',{'patient_count':patient,'doctor_count':doctor,'booking_count':booking, 'reg_doctors_list':reg_doctors_list,'reg_patient_list':reg_patient_list,'admin_name':admin_name})

@auth_admin
def admin_app_view_messages(request):
    message = Contact.objects.all()
    return render(request,'admin_app_templates/view_messages.html',{'message':message})

def clear_all(request):
    clear = Contact.objects.all()
    clear.delete()
    return redirect('admin_app:view_messages')

@auth_admin
def admin_app_doctor_page(request):
    return render(request,'admin_app_templates/doctor_page.html')

@auth_admin
def admin_app_adm_departments(request):
    dept = Departments.objects.all()
    return render(request,'admin_app_templates/adm_departments.html' ,{'department':dept})

@auth_admin
def remove_department(request,d_id):
    dep_list = Departments.objects.get(id = d_id)
    dep_list.delete()
    
    return redirect('admin_app:adm_departments')
# /////////////////////////////////////////////////////////////////////////////////////



@auth_admin
def admin_app_add_department(request):
    msg1 =''
    msg2 =''
    if request.method == 'POST':
        de_name = request.POST['department_name']
        de_description = request.POST['department_description']
        de_image = request.FILES['department_image']

        department_exist = Departments.objects.filter(dep_name = de_name).exists()

        if not department_exist:
            department = Departments(dep_name = de_name, dep_description = de_description, dep_image = de_image)
            department.save()
            msg1 = 'Department added successfully'
    
        else:
            msg2 = 'Department name already exist.'

    return render(request,'admin_app_templates/add_department.html', {'message1':msg1,'message2':msg2})


@auth_admin
def admin_app_change_department(request,e_id):
    msg=''
    error_msg =''
    department = Departments.objects.get(id=e_id)
    if request.method == 'POST':
        dep = Departments.objects.get(id = e_id)
        new_name =  request.POST['department_name']
        new_description =  request.POST['department_description']
        if 'department_image' in request.FILES:
            new_image =  request.FILES['department_image']
            dep.dep_name= new_name
            dep.dep_description = new_description
            dep.dep_image = new_image

        else:
            dep.dep_name= new_name
            dep.dep_description = new_description
        dep.save()
        return redirect('admin_app:adm_departments')
         
    else:
        error_msg = "Not Saved"


    return render(request,'admin_app_templates/change_department.html',{'edit_department':department, 'message':msg, "error_msg":error_msg})

@auth_admin
def admin_app_approve_doctor(request):
    doctor = Doctors.objects.filter(status = 'pending')

    if request.method == 'POST':
        doct_id = request.POST['doctor_id']
        doctors = Doctors.objects.get(id = doct_id)

        if 'approve' in request.POST:
            # logic when approve button clicked
            user_name = randint(1111,9999)
            password = 'sel-' + str(user_name) + str(doctors.doctor_phone)[5:]
            
            doctors.status = 'approved' #sql update query
            doctors.user_name = user_name
            doctors.password = password
          
            doctors.save()
            
           
            mail_subject = "Account Approval"
            message_body = "Hi your account has been approved by Admin, You can now login with username" + str(user_name) + " and temprorary password" + password

            
        if 'reject' in request.POST:

            doctors.status = 'reject' 
            doctors.save()
            
            mail_subject = "Account Rejected"
            message_body = "sorry we cannot approve your request"

        send_mail(
            subject = mail_subject,
            message = message_body,
            from_email = settings.EMAIL_HOST_USER,
            recipient_list= [doctors.doctor_email]
            )
    return render(request,'admin_app_templates/approve_doctor.html',{'doctor_list':doctor})


@auth_admin
def admin_app_doctor_specialisation(request):
    doctor_spec = Doctors.objects.filter(status = 'approved')
    return render(request,'admin_app_templates/doctor_specialisation.html',{'doctor_spec':doctor_spec})

@auth_admin
def admin_app_doctor_record(request):
    if 'q' in request.GET:
        q=request.GET['q']
        doctor_rec = Doctors.objects.filter(doctor_name__icontains=q, status='approved').order_by('doctor_name')
    else:
        doctor_rec = Doctors.objects.filter(status = 'approved')
    return render(request,'admin_app_templates/doctor_record.html',{'doctor':doctor_rec})

@auth_admin
def remove_doctor_record(request,d_id):
    doc_record = Doctors.objects.get(id = d_id)
    doc_record.delete()
    return redirect('admin_app:doctor_record')

@auth_admin
def admin_app_register_doctor(request):
    msg = ''
    if request.method == 'POST':
        d_name = request.POST['doc_name']
        d_email = request.POST['doc_email']
        
        d_phone = request.POST['doc_phone']
        d_address = request.POST['doc_address']
        d_gender = request.POST['doc_gender']

        dep = request.POST['doc_department']
        if 'doc_image' in request.FILES:
            d_image = request.FILES['doc_image']
            
            doctor = Doctors(doctor_name = d_name, doctor_email = d_email, doctor_department_id = dep, doctor_phone = d_phone, doctor_address = d_address, doctor_gender = d_gender, doctor_image = d_image)
        else:
            doctor = Doctors(doctor_name = d_name, doctor_email = d_email, doctor_department_id = dep, doctor_phone = d_phone, doctor_address = d_address, doctor_gender = d_gender)
        user_name = randint(1111, 9999)
        password = 'sel-' + str(user_name) + str(d_phone)[5:]
        
        doctor.status = 'approved'
        doctor.user_name = user_name
        doctor.password = password
        doctor.save()
        msg = 'Registred Successfully'

        mail_subject = "Account Approval"
        message_body = "Hi your account has been approved by Admin, You can now login with username" + str(user_name) + " and temprorary password" + password

        send_mail(
            subject = mail_subject,
            message = message_body,
            from_email = settings.EMAIL_HOST_USER,
            recipient_list= [doctor.doctor_email]
            )
            
    dep = Departments.objects.all()
    return render(request,'admin_app_templates/register_doctor.html',{'departments':dep,'message':msg})

@auth_admin
def check_email_doctor(request): # checking email of admin
    email = request.POST['doc_email']
    print(email)
    email_exist =Doctors.objects.filter(doctor_email=email).exists()
    if not email_exist:
        status = False
    else:
        status = True
    return JsonResponse({'email_exist': status})
@auth_admin
def admin_app_consultation(request, d_id):
    error_msg = ''
    success_msg = ''
    consultation_details = Consultation.objects.filter(doctor = d_id)
    doctor = Doctors.objects.filter(id = d_id).values('doctor_name')[0]['doctor_name']
    if request.method == 'POST':
        consultaion_day = request.POST['consult_day']
        consultaion_time = request.POST['frm_time'] + ' - ' + request.POST['to_time']
        record_exist = Consultation.objects.filter(doctor = d_id, day = consultaion_day, time = consultaion_time).exists()
        if not record_exist :
            new_record = Consultation(doctor_id = d_id,day = consultaion_day, time = consultaion_time)
            new_record.save()
            success_msg = 'Record Added Succesfully'
        else:
            error_msg = 'Record Already Added'
   
    context = {
            'doctor_name': doctor,
            'consultation_details':consultation_details,
            'success_msg':success_msg,
            'error_msg':error_msg
            
            }
    
    return render(request,'admin_app_templates/consultation.html',context)

def check_day(request): # checking consult day and time is repeating or not
    c_day = request.POST.get('consult_day')
    day_exist = Consultation.objects.filter(day=c_day).exists()
    status = {'day_exist': day_exist}
    return JsonResponse(status)



@auth_admin
def delete_consultation(request,c_id):
    details = Consultation.objects.get(id = c_id)
    details.delete()
    messages.success(request, 'Deleted successfully')
    return redirect(reverse_lazy('admin_app:consultation', args=[details.doctor_id]))

@auth_admin
def edit_consultation(request, d_id):
    edit_cons = Consultation.objects.get(id=d_id)
    print("time",edit_cons.day)
    time=edit_cons.time.split('-')
    print(time[0],time[1])
    context = {
        # 'edit_consult':time
        'edit_cons':edit_cons,
        "time1":time[0],
        "time2":time[1]
    }
    return render(request, 'admin_app_templates/consultation.html',context)

@auth_admin
def update_consultation(request, d_id):
    if request.method == 'POST':
        ed_cons = Consultation.objects.get(id=d_id)
        ed_cons.day = request.POST['consult_day']
        ed_cons.time = request.POST['frm_time'] + ' - ' + request.POST['to_time']
        ed_cons.save()
        
        messages.success(request, 'Updated Successfully')
    return redirect(reverse_lazy('admin_app:consultation', args=[ed_cons.doctor_id]))






# /////////////////////////////Patient Section //////////////////////////////////////////////////
@auth_admin
def admin_app_approve_patient(request):
    patient = Booking.objects.filter(status = 'pending')

    if request.method == 'POST':
        pat_id = request.POST['patient_id']
        patients = Booking.objects.get(id = pat_id)

        if 'approve' in request.POST:
          
            
            patients.status = 'booked' #sql update query
           
          
            patients.save()
            
           
            mail_subject = "Doctor Booking Approval"
            message_body = "Hi, Your appointment booking has been approved"

            
        if 'reject' in request.POST:

            patients.status = 'reject' 
            patients.save()
            
            mail_subject = "Booking Appointment Rejected"
            message_body = "sorry we cannot approve your request"

        send_mail(
            subject = mail_subject,
            message = message_body,
            from_email = settings.EMAIL_HOST_USER,
            recipient_list= [patients.patient_email]
            )
    return render(request,'admin_app_templates/approve_patient.html',{'patient_list':patient})

@auth_admin
def admin_app_patient_registered(request):
    patient = Patient.objects.all()
    return render(request,'admin_app_templates/patient_registered.html',{'reg_patient':patient})

@auth_admin
def remove_regpatient_record(request,p_id):
    pat_record = Patient.objects.get(id = p_id)
    pat_record.delete()
    return redirect('admin_app:patient_registered')

@auth_admin
def admin_app_view_patients(request):
    patient = Booking.objects.filter(status = 'booked')
    return render(request,'admin_app_templates/view_patients.html',{'view_patient':patient})

@auth_admin
def remove_patient_record(request,p_id):
    pat_record = Booking.objects.get(id = p_id)
    pat_record.delete()
    return redirect('admin_app:view_patients')


@auth_admin
def admin_app_consulted_patient(request):  #For searching
    if 'q' in request.GET:
        q=request.GET['q']
        patient = Booking.objects.filter(patient_name__icontains=q, status='consulted').order_by('patient_name')
    else:
        patient = Booking.objects.filter(status = 'consulted')
    return render(request,'admin_app_templates/consulted_patient.html',{'view_patient':patient})

@auth_admin
def remove_consulted_patient(request,p_id):
    pat_record = Booking.objects.get(id = p_id)
    pat_record.delete()
    return redirect('admin_app:view_patients')

@auth_admin
def admin_app_book_patient(request):
    msg = ''
    doctors = None
   
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
        ref_no = 'REF-'+ str(randint(1000,9999))+ pphone[6:]
        pdescription = request.POST['pat_description']
        paddress = request.POST['pat_address']
        doctor = Doctors.objects.get(id=pdoctor)
        booking = Booking(patient_name = pname, patient_email = pemail, patient_phone = pphone, patient_gender = pgender,birth_date =pbirth ,patient_age = page, booking_date = pdate, booking_time = ptime, doctor_name = doctor, patient_description = pdescription, patient_address = paddress,reference_no = ref_no)
        booking.status = 'approved'
        booking.save()
        msg = 'Booked Successfully..'
        mail_subject = "Doctor Booking Approval"
        message_body = "Hi, Your appointment booking has been approved"
        send_mail(
            subject = mail_subject,
            message = message_body,
            from_email = settings.EMAIL_HOST_USER,
            recipient_list= [booking.patient_email]
            )

    else:
        doctors = Doctors.objects.filter(status = 'approved') 
        
   
    return render(request,'admin_app_templates/book_patient.html',{'doctor':doctors, 'message':msg})

@auth_admin
def admin_app_patient_page(request):
    
    return render(request,'admin_app_templates/patient_page.html')


@auth_admin
def admin_app_appointments(request):
    patient = Booking.objects.filter(status = 'booked')
    return render(request,'admin_app_templates/appointments.html',{'view_patient':patient})



def admin_logout(request):
    if 'admin' in request.session:
        request.session.pop('admin')
    return redirect('common_app:home')
