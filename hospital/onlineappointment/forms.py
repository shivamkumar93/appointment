from django import forms

from .models import *

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = "__all__"

class DoctorForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Doctor
        fields = ['name','department','image','qualification','consultation_fees','available']

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ['appointment', 'user']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor','appointment_date', 'appointment_time']