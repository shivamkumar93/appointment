from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import login, authenticate


def loginDoctor(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('doctorappointmentlist')
    
    return render(request, 'doctor/login.html')

def doctorappointmentlist(request):
    doctor = Doctor.objects.get(user = request.user)
    appointment = Appointment.objects.filter(doctor=doctor)
    return render(request, 'doctor/doctorappointmentlist.html', {'doctor':doctor, 'appointment':appointment})