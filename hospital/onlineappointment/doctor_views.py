from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import login, authenticate
from django.utils.dateparse import parse_date


def loginDoctor(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('doctorappointmentlist')
    
    return render(request, 'doctor/login.html')

def doctorappointmentlist(request):
    doctor = Doctor.objects.get(user = request.user)
    appointments = Appointment.objects.filter(doctor=doctor).order_by('appointment_date', 'appointment_time')

    date = request.GET.get('date')

    if date:
        appointments = appointments.filter(appointment_date=parse_date(date)).order_by('appointment_time')

    return render(request, 'doctor/doctorappointmentlist.html', {'doctor':doctor, 'appointments':appointments})

