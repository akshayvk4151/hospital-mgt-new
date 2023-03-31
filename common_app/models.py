from django.db import models


# Create your models here.

class Patient(models.Model):
    patient_name = models.CharField(max_length=50)
    patient_mobile = models.BigIntegerField()
    patient_address = models.CharField(max_length=200)
    patient_email = models.CharField(max_length=40)
    patient_password = models.CharField(max_length=10,default='')
    status = models.CharField(max_length=20, default='active')

    class Meta:
        db_table = 'patient'


class Departments(models.Model):
    dep_name = models.CharField(max_length=100)
    dep_description = models.TextField()
    dep_image = models.ImageField(upload_to='department/')

    class Meta:
        db_table = 'department'


class Doctors(models.Model):
    doctor_name = models.CharField(max_length=50)
    doctor_email = models.CharField(max_length=40)
    doctor_department = models.ForeignKey(Departments,on_delete=models.CASCADE)
    doctor_phone = models.BigIntegerField()
    doctor_address = models.CharField(max_length=200)
    user_name = models.IntegerField(default=0)
    password = models.CharField(max_length=40, default='')
    doctor_gender = models.CharField(max_length=15)
    doctor_image = models.ImageField(upload_to='doctor/',default='static/images/dummy-user.png')
    status = models.CharField(max_length=20, default='pending')

    class Meta:
        db_table = 'doctors'


class Admin(models.Model):
    admin_name = models.CharField(max_length=40)
    admin_email =  models.CharField(max_length=40)
    admin_password = models.CharField(max_length=10,default='')

    class Meta:
        db_table = 'admin'


class Contact(models.Model):
    name = models.CharField(max_length=40)
    phone = models.BigIntegerField()
    remark = models.CharField(max_length=300)

    class Meta:
        db_table = 'contact'
