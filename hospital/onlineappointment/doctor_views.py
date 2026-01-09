from django.shortcuts import render, redirect
from .forms import *

def department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect(department)
    else:
        form = DepartmentForm()

    return render(request, 'doctor/departmentform.html', {'form':form})

def createdoctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect(createdoctor)
    else:
        form = DoctorForm()
    return render(request, 'doctor/doctorform.html', {'form':form})

def doctorappointmentlist(request):
    return render(request, 'doctorappointmentlist.html')