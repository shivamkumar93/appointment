from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from .forms import *
import razorpay
from django.conf import settings
import json 
from django.http import JsonResponse

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


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
    return render(request, 'user/appointmentdate.html', {'doctor':doctor})

def patientdetails(request, appointment_id):
    form = PatientForm(request.POST or None)
    if form.is_valid():
        patient = form.save(commit=False)

        patient.appointment = get_object_or_404(Appointment, id=appointment_id)
        patient.save()
        return redirect('appointmentdetails', id=patient.appointment.id)
    return render(request, 'user/patientaddress.html',{'form':form})

def appointmentdetails(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    doctor = appointment.doctor
    patient = Patient.objects.filter(appointment=appointment).first()

    return render(request, 'user/appointmentdetails.html', {'appointment': appointment, 'doctor': doctor, 'patient': patient})

def payment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id = appointment_id)
    patient = Patient.objects.get(appointment=appointment)

    amount = appointment.doctor.consultation_fees * 100

    order = client.order.create({"amount":amount, "currency":"INR", "payment_capture":1})

    payment = Payment.objects.create(appointment=appointment, patient=patient, doctor = appointment.doctor, razorpay_order_id=order['id'], status='created')
    context = {
        "payment": payment,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "amount": amount,
        "currency": "INR"
    }
    return render(request, 'user/payment.html', context)

def payment_verify(request):
    data = json.loads(request.body)

    razorpay_order_id = data.get('razorpay_order_id')
    razorpay_payment_id= data.get('razorpay_payment_id')
    razorpay_signature = data.get('razorpay_signature')

    payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)

    try:
        client.utility.verify_payment_signature({'razorpay_order_id':razorpay_order_id, 'razorpay_payment_id':razorpay_payment_id, 'razorpay_signature':razorpay_signature})
        
        payment.razorpay_payment_id = razorpay_payment_id
        payment.razorpay_signature = razorpay_signature
        payment.status = 'success'
        payment.save()

        payment.appointment.status = 'confirmed'
        payment.appointment.save()
        return JsonResponse({"message":"appointment approved and payment success"})
    
    except:
        payment.status = 'failed'
        payment.save()
        return JsonResponse({"message":"payment failed"})