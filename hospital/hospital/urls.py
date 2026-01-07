
from django.contrib import admin
from django.urls import path
from onlineappointment.views import *
from onlineappointment.doctor_views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    #user penal
    path('', home, name='homepage'),
    path('doctorslist/',doctorslist, name="doctorlist"),
    path('appointmentdate/<int:doctor_id>/',appointmentdate, name="appointmentdate"),
    path('patientaddress/<int:appointment_id>/', patientdetails, name='patientdetail'),
    # doctor penal
    path('department/',department, name="departmentform" ),
    path('doctorform/',doctor, name="doctorform" ),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

