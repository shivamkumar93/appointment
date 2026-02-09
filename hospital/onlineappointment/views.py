from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.urls import reverse
from .forms import *
import razorpay
from django.conf import settings
import json 
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.utils import timezone
from datetime import timedelta
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))



# Create your views here.
def home(request):
    doctors = Doctor.objects.all()
    return render(request, 'user/home.html', {'doctors':doctors})

def doctorslist(request):
    departments = Department.objects.all()
    doctors = Doctor.objects.all()

    department_id = request.GET.get('department')
    if department_id:
        doctors = doctors.filter(department_id=department_id)

    return render(request, 'user/doctorslist.html', {'departments':departments, 'doctors':doctors})

def appointmentdate(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    if request.method == 'POST':
        date = request.POST.get('appointment_date')
        time = request.POST.get('appointment_time')

        exists = Appointment.objects.filter(doctor=doctor,appointment_date = date, appointment_time = time, status = 'confirmed').exists()
        if exists:
            return render(request, 'user/appointmentdate.html', {
                'doctor': doctor, 'error': "This slot is already booked. Please choose another time."})

        appointment = Appointment.objects.create(doctor=doctor, appointment_date = date, appointment_time= time, status = 'pending')
        return redirect('patientdetail', appointment_id=appointment.id)
    return render(request, 'user/appointmentdate.html', {'doctor':doctor})

def patientdetails(request, appointment_id):
    form = PatientForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['phone_number']
        
        user, created = User.objects.get_or_create( username=username)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)

        patient = form.save(commit=False)
        patient.user = user
        patient.save()
        appointment = get_object_or_404(Appointment, id=appointment_id)
        appointment.patient = patient
        appointment.save()
        return redirect('appointmentdetails', id=appointment.id)
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
        return JsonResponse({"message":"success", "redirect_url":reverse('patientAppointmentinfo')})
    except:
        payment.status = 'failed'
        payment.save()
        return JsonResponse({"message":"payment failed"})
    
def success(request):
    return render(request, 'user/success.html')

def loginpatient(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user,_ = User.objects.get_or_create(username=username)
        if not user:
           return render(request, 'user/patientlogin.html')
        login(request, user)
        return redirect('patientAppointmentinfo')
    return render(request, 'user/patientlogin.html')

def patientinfo(request):
    appointments = Appointment.objects.filter(patient__user=request.user)
    return render(request, 'user/patientappointmentinfo.html',{'appointments':appointments})

def editpatientdetails(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = PatientForm(request.POST , instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patientAppointmentinfo')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'user/editpatientdetail.html', {'form':form})

def paymentdetail(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    paymentinfos = appointment.payment_set.all()
    return render(request, 'user/paymentdetails.html', {'appointment':appointment, 'paymentinfos':paymentinfos})



def paymentRefund(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    payment = Payment.objects.get(appointment=appointment)

    if payment.status == 'success' and payment.razorpay_payment_id:
        try:
            total_amount = payment.doctor.consultation_fees  
            cancellation_charge = total_amount * 10 / 100
            refund_amount = total_amount - cancellation_charge

           
            refund_amount_paise = int(refund_amount * 100)

            print(refund_amount_paise)
            refund = client.payment.refund(payment.razorpay_payment_id, {"amount": refund_amount_paise } )

            if refund['status'] == 'processed':
                payment.status = 'refund'
                payment.save()
                appointment.status = 'cancelled'
                appointment.save()

                messages.success(
                    request,
                    f'Appointment cancelled. ₹{cancellation_charge} charged, ₹{refund_amount} refunded.'
                )

        except :
            pass
    return redirect('paymentdetails')



# def paymentRefund(request, id):
#     appointment = get_object_or_404(Appointment, id=id)
#     payment = get_object_or_404(Payment, appointment=appointment)

#     today = timezone.localdate()
#     appointment_date = appointment.appointment_date  # DateField

#     # next-day cancel rule
#     if today < appointment_date + timedelta(days=1):
#         messages.error(request, 'Appointment can be cancelled only after 24 hours')
#         return redirect('patientAppointmentinfo')

#     if payment.status != 'success' or not payment.razorpay_payment_id:
#         messages.error(request, 'Payment not eligible for refund')
#         return redirect('paymentdetails')

#     try:
#         # consultation fees in paise
#         total_amount = int(payment.doctor.consultation_fees * 100)

#         # 10% cancellation charge
#         charge = int(total_amount * 0.10)
#         refund_amount = total_amount - charge

#         refund = client.payment.refund(
#             payment.razorpay_payment_id,
#             {
#                 "amount": refund_amount
#             }
#         )

#         if refund['status'] in ['processed', 'pending']:
#             payment.status = 'refund'
#             payment.save()

#             appointment.status = 'cancelled'
#             appointment.save()

#             messages.success(
#                 request,
#                 'Appointment cancelled successfully. 10% cancellation charge applied.'
#             )

#     except Exception as e:
#         messages.error(request, f'Refund failed: {str(e)}')

#     return redirect('paymentdetails')


