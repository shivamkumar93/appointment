from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth import login, authenticate, logout
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

def doctoreditappointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST , instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('doctorappointmentlist')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'doctor/doctoreditappointment.html',{'form':form})

def logoutdoctor(request):
    logout(request)
    return redirect('logindoctor')