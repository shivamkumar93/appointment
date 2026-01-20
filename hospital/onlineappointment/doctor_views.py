from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth import login, authenticate, logout
from django.utils.dateparse import parse_date
from django.contrib import messages
from .views import *



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

from django.db import transaction

def doctoreditappointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)

    if request.method == 'POST':
        old_date = appointment.appointment_date
        old_time = appointment.appointment_time
        old_status = appointment.status
        old_doctor = appointment.doctor
        old_patient = appointment.patient

        form = AppointmentForm(request.POST, instance=appointment)

        if form.is_valid():
            with transaction.atomic():
                AppointmentHistory.objects.create(
                    appointment=appointment,doctor=old_doctor,patient=old_patient,
                    old_date=old_date, old_time=old_time, old_status=old_status
                )
                form.save()
            return redirect('doctorappointmentlist')

    else:
        form = AppointmentForm(instance=appointment)

    return render(request,'doctor/doctoreditappointment.html', {'form': form})


def logoutdoctor(request):
    logout(request)
    return redirect('logindoctor')

    
def cancelAndrefund(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    payment = get_object_or_404(Payment, appointment=appointment)

    if payment.status == 'success' and payment.razorpay_payment_id:
        try:
            refund = client.payment.refund(payment.razorpay_payment_id)

            if refund['status'] == 'processed':
                payment.status = 'refund'
                payment.save()
                appointment.status = 'cancelled'
                appointment.save()

                messages.success(request, "Appointment cancelled & refunded")
                return redirect('doctorappointmentlist')

        except Exception as e:
            messages.error(request, f"Refund failed: {str(e)}")
            return redirect('doctorappointmentlist')

    messages.error(request, "Refund not possible")
    return redirect('doctorappointmentlist')
