from django.db import models

from common_app.models import Doctors, Patient

# Create your models here.

class Booking(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE,null=True )
    patient_name = models.CharField(max_length=50)
    patient_email = models.CharField(max_length=40)
    patient_phone = models.BigIntegerField()
    patient_gender = models.CharField(max_length=15)
    birth_date =  models.DateField(null=True)
    patient_age = models.PositiveIntegerField(null=True, blank=True)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    reference_no = models.CharField(max_length=40, default='')
    doctor_name = models.ForeignKey(Doctors,on_delete=models.CASCADE)
    patient_description = models.CharField(max_length=200)
    patient_address = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=20, default='pending')

    class Meta:
        db_table = 'booking'