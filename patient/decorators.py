from django.http import HttpResponseRedirect 
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
def auth_patient(func) :
    def wrapper (request, *args, **kwargs):


        if 'patient' in request.session:
            return func (request, *args, **kwargs)
            
        else:
            return redirect('common_app:patient_login')

            
    return wrapper