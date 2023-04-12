from audioop import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from.models import Admin, Contact, Departments, Doctors, Patient
from django.http import JsonResponse
from django.contrib.auth import authenticate, login

# Create your views here.

def common_app_index(request):
    return render(request,'common_app_templates/index.html')



def common_app_about(request):
    return render(request,'common_app_templates/about.html')

def common_app_contact(request):
    msg = ''
    if request.method == 'POST':
        pname = request.POST['name']
        pmobile = request.POST['mobile'] 
        premark = request.POST['remark'] 
        client = Contact(name = pname, phone = pmobile, remark = premark)
        client.save()
        msg = 'Message Send!'

    return render(request,'common_app_templates/contact.html',{'message':msg})



# ////////////////////////Patient section///////////////////////////////////////

def common_app_patient_click(request):
    return render(request,'common_app_templates/patient_click.html')

def common_app_patient_login(request):
    msg = ''
    if request.method == 'POST':
        email = request.POST['p_email']
        password = request.POST['p_password'] 

        try:
            patient = Patient.objects.get(patient_email = email, patient_password = password)
            request.session['patient'] = patient.id
            print(request.session['patient'])
            return redirect('patient:index')
        except:
            msg = 'Email or Password is incorrect'
    return render(request,'common_app_templates/patient_login.html',{'message':msg})

def common_app_patient_register(request):
    
    msg2 = ''
    if request.method == 'POST':
        pat_name = request.POST['p_name']
        pat_mobile = request.POST['p_mobile']
        pat_address = request.POST['p_address']
        pat_email = request.POST['p_email']
        pat_password = request.POST['p_password']
        email_exist = Patient.objects.filter(patient_email = pat_email).exists()
        if not email_exist:

            patient = Patient(patient_name = pat_name, patient_mobile = pat_mobile, patient_address = pat_address, patient_email= pat_email, patient_password= pat_password)
            patient.save()
            msg2 = 'You are Successfully Registred !'

       
        
    return render(request,'common_app_templates/patient_register.html',{'message2':msg2})


def check_email(request):  #checking email of patient
    email = request.POST['p_email']
    print(email)
    email_exist =Patient.objects.filter(patient_email=email).exists()
    if not email_exist:
        status = False
    else:
        status = True
    return JsonResponse({'email_exist': status})

def check_email_admin(request): # checking email of admin
    email = request.POST['a_email']
    print(email)
    email_exist =Admin.objects.filter(admin_email=email).exists()
    if not email_exist:
        status = False
    else:
        status = True
    return JsonResponse({'email_exist': status})

def check_email_doctor(request): # checking email of admin
    email = request.POST['doc_email']
    print(email)
    email_exist =Doctors.objects.filter(doctor_email=email).exists()
    if not email_exist:
        status = False
    else:
        status = True
    return JsonResponse({'email_exist': status})


def common_app_doctor_click(request):
    return render(request,'common_app_templates/doctor_click.html')

def common_app_doctors_login(request):
    msg=''
    if request.method == 'POST':
        
        username = request.POST['user_name']
        password = request.POST['password']

        try:
            doctor = Doctors.objects.get(user_name = username,password = password)
            request.session['doctor'] = doctor.id
            print( request.session['doctor'])
            return redirect('doctor:index')
            
        except Exception as e:
            
            msg = 'username or password not match'

    return render(request,'common_app_templates/doctors_login.html',{'message':msg})



def common_app_doctors_register(request):
    msg1=''
    msg2=''
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
        doctor.save()
        msg1 = 'You are Successfully Registred'
        return redirect('common_app:doc_logincheck', doctor_id=doctor.id)
    dep = Departments.objects.all()
    return render(request,'common_app_templates/doctors_register.html',{'departments':dep , 'message1':msg1, 'message2':msg2})

def common_app_doc_logincheck(request,doctor_id): # for name
    doctor = Doctors.objects.get( id=doctor_id)
    return render(request,'common_app_templates/doc_logincheck.html', {'doctor': doctor})


def common_app_department(request):
    dic_dept = Departments.objects.all()
    for dept in dic_dept:

        dept.image_url = dept.dep_image.url

    return render(request,'common_app_templates/department.html', {'dic_dept':dic_dept})


def common_app_doctors(request):
    doctor = Doctors.objects.filter(status = 'approved')
    for doc in doctor:

        doc.image_url = doc.doctor_image.url
    return render(request,'common_app_templates/doctors.html',{'doctors':doctor})

def common_app_admin_register(request):
    msg = ''
    if request.method == 'POST':
        adm_name = request.POST['a_name']
        adm_email = request.POST['a_email']
        adm_password = request.POST['a_password']
        email_exist = Admin.objects.filter(admin_email = adm_email).exists()
        if not email_exist:

            admin = Admin(admin_name = adm_name, admin_email= adm_email, admin_password = adm_password)
            admin.save()
            msg = 'You are Successfully Registred !'
            # return redirect('common_app:admin_success')
            
    return render(request,'common_app_templates/admin_register.html',{'message':msg})

def common_app_admin_login(request):
    msg = ''
    if request.method == 'POST':
        email = request.POST['ad_email']
        password = request.POST['ad_password'] 

        try:
            admin = Admin.objects.get(admin_email = email, admin_password = password)
            request.session['admin'] = admin.id
            print(request.session['admin'])
            return redirect('admin_app:index')
        except:
            msg = 'Email or Password is incorrect'
   
    return render(request,'common_app_templates/admin_login.html',{'message':msg})



def common_app_admin_click(request):
    return render(request,'common_app_templates/admin_click.html')


     
    

    
    
        
  