from django import forms

from .models import *

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = "__all__"

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = "__all__"

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = "__all__"