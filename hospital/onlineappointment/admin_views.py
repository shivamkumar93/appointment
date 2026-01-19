from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.models import User
from datetime import date
from django.contrib import messages

from .forms import *

def dashboard(request):
    today = date.today()
    data = {}
    data['total'] = Appointment.objects.filter(status='confirmed').count()
    data['patient'] = Patient.objects.all().count()
    data['doctor'] = Doctor.objects.all().count()
    data['today'] = Appointment.objects.filter(appointment_date=today).count()
    data['appointments'] = Appointment.objects.filter(appointment_date=today)
    return render(request, 'admin/dashboard.html', data)

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
    appointments = Appointment.objects.all()
    return render(request, 'admin/totalAppointment.html', {'appointments':appointments})

def editAppointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    if request.method == 'POST':
        old_date = appointment.appointment_date
        old_time = appointment.appointment_time
        old_doctor = appointment.doctor
        old_patient = appointment.patient
        old_status = appointment.status

        form = AppointmentForm(request.POST , instance=appointment)
        if form.is_valid():
            AppointmentHistory.objects.create(appointment=appointment, doctor=old_doctor, patient = old_patient, old_date=old_date, old_time=old_time, old_status=old_status)
            form.save()
            return redirect('totalappointmentlist')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'admin/editappointment.html', {'form':form})

def cancleAppointmentadmin(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    payment = Payment.objects.get(appointment=appointment)

    if payment.status == 'success':
        payment.status = 'refund'
        payment.save()

    appointment.status = 'cancelled'
    appointment.save()
    messages.success(request, "appointment cancelled")
    return redirect('totalappointmentlist')
