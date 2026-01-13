
from django.contrib import admin
from django.urls import path
from onlineappointment.views import *
from onlineappointment.doctor_views import *
from django.conf import settings
from django.conf.urls.static import static
from onlineappointment.admin_views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    #user penal
    path('', home, name='homepage'),
    path('doctorslist/',doctorslist, name="doctorlist"),
    path('appointmentdate/<int:doctor_id>/',appointmentdate, name="appointmentdate"),
    path('patientaddress/<int:appointment_id>/', patientdetails, name='patientdetail'),
    path('appointmentdetails/<int:id>/', appointmentdetails, name="appointmentdetails" ),
    path('pay/<int:appointment_id>/', payment, name='payment'),
    path('payment_verify/', payment_verify, name="paymentVerify"),
    path('patientlogin/', loginpatient, name='patientlogin'),
    path('patientappointmentinfo/', patientinfo, name='patientAppointmentinfo'),
    # doctor penal
    
    path('successpage/', success, name="successpage"),
    path('doctorappointmentlist/', doctorappointmentlist, name="doctorappointmentlist"),
    path('logindoctor/', loginDoctor, name='logindoctor'),

    # admin penal
    path('dashboard/', dashboard, name='dashboard'),
    path('department/',department, name="departmentform" ),
    path('doctorform/',createdoctor, name="doctorform" ),
    path('totaldoctor/', totalDoctor, name="totaldoctorlist"),
    path('totalpatient/', totalPatient, name="totalpatientlist"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

