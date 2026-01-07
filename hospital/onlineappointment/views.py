from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from .forms import *


# Create your views here.
def home(request):
    doctors = Doctor.objects.all()
    return render(request, 'user/home.html', {'doctors':doctors})

def doctorslist(request):
    data = {}
    data['departments'] = Department.objects.all()
    data['doctors'] = Doctor.objects.all()
    return render(request, 'user/doctorslist.html', data)

def appointmentdate(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    if request.method == 'POST':
        date = request.POST.get('appointment_date')
        time = request.POST.get('appointment_time')

        appointment = Appointment.objects.create(doctor=doctor, appointment_date = date, appointment_time= time, status = 'pending')
        return redirect('patientdetail', appointment_id=appointment.id)
    return render(request, 'user/appointmentdate.html')

def patientdetails(request, appointment_id):
    form = PatientForm(request.POST or None)
    if form.is_valid():
        patient = form.save(commit=False)

        patient.appointment = Appointment.objects.get(id=appointment_id)
        patient.save()
    return render(request, 'user/patientaddress.html',{'form':form})