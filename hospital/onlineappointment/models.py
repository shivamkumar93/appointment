from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Department(models.Model):
    title = models.CharField(max_length=100)
    def __str__(self):
        return self.title
    
class Doctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="media/")
    qualification = models.CharField(max_length=100)
    consultation_fees = models.IntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Patient(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE, null=True, blank=True)

    fullname = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    age = models.IntegerField()
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    pincode = models.IntegerField()
    state = models.CharField(max_length=20)

    def __str__(self):
        return self.fullname

    
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'pending'),
        ('confirmed', 'confirmed'),
        ('completed', 'completed'),
        ('cancelled', 'cancelled')
    ]
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending' )

    def __str__(self):
        return f"{self.doctor.name}- {self.appointment_date}"


class Payment(models.Model):
    PAYMENT_STATUS = (
        ('created','created'),
        ('success','success'),
        ('failed','failed')
    )
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    razorpay_order_id = models.CharField(max_length=50, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='created', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.patient.fullname}-{self.doctor.name}"