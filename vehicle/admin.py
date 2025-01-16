from django.contrib import admin
from .models import RiderRequest,Vehicle

# Register your models here.


class RiderRequestAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','car_types','address','geolocation','status','cancel']
    
    def first_name(self,obj):
        return obj.customer.user.first_name
    
    def last_name(self,obj):
        return obj.customer.user.last_name
    
    
admin.site.register(RiderRequest,RiderRequestAdmin)

class VehicleAdmin(admin.ModelAdmin):
    list_display=['drive','registration_number','vehicle_model','image']
    
    
admin.site.register(Vehicle,VehicleAdmin,)