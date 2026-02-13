from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.models import User
from datetime import date
from django.contrib import messages
from .doctor_views import *
from .forms import *
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    today = date.today()
    data = {}
    data['total'] = Appointment.objects.filter(status='confirmed').count()
    data['patient'] = Patient.objects.all().count()
    data['doctor'] = Doctor.objects.all().count()
    data['today'] = Appointment.objects.filter(appointment_date=today).count()
    data['cancel'] = Appointment.objects.filter(status='cancelled').count()
    data['appointments'] = Appointment.objects.filter(appointment_date=today)
    data['payment'] = Payment.objects.all().count()
    data['refund'] = Payment.objects.filter(status = 'refund').count()
    return render(request, 'admin/dashboard.html', data)

@login_required
def department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect(department)
    else:
        form = DepartmentForm()
    departments = Department.objects.all()
    return render(request, 'admin/departmentform.html', {'form':form, 'departments':departments})

@login_required
def deletedepartment(request, id):
    dep = Department.objects.get(id=id)
    dep.delete()
    return redirect('departmentform')

@login_required
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

@login_required
def totalDoctor(request):
    doctors = Doctor.objects.all()
    return render(request, 'admin/totaldoctor.html', {'doctors':doctors})

def deleteDoctor(request, id):
    doctor = Doctor.objects.get(id=id)
    doctor.delete()
    return redirect('totaldoctorlist')

@login_required
def totalPatient(request):
    patients = Patient.objects.all()
    return render(request, 'admin/totalpatient.html', {'patients':patients})

@login_required
def totalAppointment(request):
    appointments = Appointment.objects.all()
    return render(request, 'admin/totalAppointment.html', {'appointments':appointments})

@login_required
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
            appointment_reschedule(appointment.patient, appointment)
            return redirect('totalappointmentlist')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'admin/editappointment.html', {'form':form})


@login_required
def cancleAppointmentadmin(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    payment = Payment.objects.get(appointment=appointment)

    if payment.status == 'success' and payment.razorpay_payment_id:
        try:
            refund = client.payment.refund(payment.razorpay_payment_id)
            if refund['status'] == 'processed':
                payment.status = 'refund'
                payment.save()
                appointment.status = 'cancelled'
                appointment.save()
        except:
            pass
    
    messages.success(request, "appointment cancelled")
    return redirect('totalappointmentlist')

@login_required
def offlineAppointment(request):
    appointments = Appointment.objects.filter(payment_mode = 'offline')
    return render(request, 'admin/offlineappointment.html', {'appointments':appointments})

@login_required
def conformofflineAppointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    appointment.status = 'confirmed'
    appointment.save()
    return redirect('offlineappointment')