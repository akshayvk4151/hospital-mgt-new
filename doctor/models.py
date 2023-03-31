from django.db import models

from patient.models import Booking

# Create your models here.


class Prescription(models.Model):
    booking = models.ForeignKey(Booking,on_delete=models.CASCADE)
    
    diagnosis = models.CharField(max_length=300)
    medication_name =  models.CharField(max_length=50)
    purpose = models.CharField(max_length=50)
    dosage = models.CharField(max_length=40)
    route = models.CharField(max_length=30)
    frequency = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='active')

    class Meta:
        db_table = 'prescriptions'

    
