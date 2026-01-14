from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.models import User
from datetime import date

from .forms import *

def dashboard(request):
    today = date.today()
    appointments = Appointment.objects.filter(appointment_date=today)
    return render(request, 'admin/dashboard.html', {'appointments':appointments})

def department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect(department)
    else:
        form = DepartmentForm()

    return render(request, 'admin/departmentform.html', {'form':form})

def createdoctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = User.objects.create_user(username=username, password=password)
            doctor = form.save(commit=False)
            doctor.user = user
            doctor.save()
            return redirect(createdoctor)
    else:
        form = DoctorForm()
    return render(request, 'admin/doctorform.html', {'form':form})

def totalDoctor(request):
    doctors = Doctor.objects.all()
    return render(request, 'admin/totaldoctor.html', {'doctors':doctors})

def totalPatient(request):
    patients = Patient.objects.all()
    return render(request, 'admin/totalpatient.html', {'patients':patients})

def totalAppointment(request):
    appointments = Appointment.objects.filter(status='confirmed').order_by('appointment_date','appointment_time')
    return render(request, 'admin/totalAppointment.html', {'appointments':appointments})