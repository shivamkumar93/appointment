from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


def appointment_reschedule(patient, appointment):
    
    subject = "Appointment Rescheduled"
    message = f""" Dear {patient.fullname},Your appointment has been rescheduled.
        New Date: {appointment.appointment_date} New Time: {appointment.appointment_time}
        Thank you, Hospital Team """

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [patient.email],
        fail_silently=False
    )
