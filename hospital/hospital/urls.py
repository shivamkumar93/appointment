
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
    path('editpatientdetail/<int:patient_id>/', editpatientdetails, name='editpatientdetails'),
    path('successpage/', success, name="successpage"),
    path('paymentdetails/<int:id>/', paymentdetail, name="paymentdetails"),
    path('offlinepayment/<int:id>/', offlinePayment, name="offlinepayment"),
    path('paymentRefund/<int:id>/', paymentRefund, name="paymentRefund" ),
    path('editappointmentdate/<int:id>/', appointmentEdit, name="editappointmentbypatient" ),
    # doctor penal
    
    path('doctorappointmentlist/', doctorappointmentlist, name="doctorappointmentlist"),
    path('logindoctor/', loginDoctor, name='logindoctor'),
    path('logoutdoctor/', logoutdoctor, name='logoutdoctor'),
    path('doctoreditappointment/<int:id>/', doctoreditappointment, name='doctoreditappointment'),
    path('canclledappointment/<int:id>/', cancelAndrefund, name='canclledappointment'),


    # admin penal
    path('dashboard/', dashboard, name='dashboard'),
    path('department/',department, name="departmentform" ),
    path('department/delete/<int:id>/',deletedepartment, name="deletedepartment" ),
    path('doctorform/',createdoctor, name="doctorform" ),
    path('totaldoctor/', totalDoctor, name="totaldoctorlist"),
    path('doctor/delete/<int:id>/', deleteDoctor, name="deletedoctor"),
    path('totalpatient/', totalPatient, name="totalpatientlist"),
    path('totalappointment/', totalAppointment, name="totalappointmentlist"),
    path('offlineappointment/', offlineAppointment, name="offlineappointment"),
    path('conformofflineappointment/<int:id>/', conformofflineAppointment, name="conformofflineappointment"),
    path('editappointment/<int:id>/', editAppointment, name="editappointment"),
    path('admincancleappointment/<int:id>/', cancleAppointmentadmin, name="admincancleappointment")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

