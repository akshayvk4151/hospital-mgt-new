from django.db import models

from common_app.models import Doctors

# Create your models here.





class Consultation(models.Model) : 

    doctor = models.ForeignKey(Doctors, on_delete = models.CASCADE)
    day = models.CharField(max_length = 20)
    time = models.CharField(max_length = 20)
    status = models.CharField(max_length = 20, default = 'available')
    
    class Meta :
        db_table = 'consult'