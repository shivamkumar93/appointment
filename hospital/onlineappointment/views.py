from django.shortcuts import render
from .models import *


# Create your views here.
def home(request):
    doctors = Doctor.objects.all()
    return render(request, 'user/home.html', {'doctors':doctors})

def appointmentdate(request):
    data = {}
    data['departments'] = Department.objects.all()
    data['doctors'] = Doctor.objects.all()
    return render(request, 'user/appointment.html', data)