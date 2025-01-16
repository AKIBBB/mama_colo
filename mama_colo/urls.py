
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contact_us/',include('contactus.urls')),
    path('service/',include('service.urls')),
    path('customer/',include('customer.urls')),
    path('driver/',include('driver.urls')),
    path('vehicle/',include('vehicle.urls')),
]

urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
