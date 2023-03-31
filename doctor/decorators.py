from django.http import HttpResponseRedirect 
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
def auth_doctor(func) :
    def wrapper (request, *args, **kwargs):


        if 'doctor' in request.session:
            return func (request, *args, **kwargs)
            
        else:
            return redirect('common_app:doctors_login')

            
    return wrapper