from django.contrib import admin
from.import models
from .models import Driver

# Register your models here.
class DriverAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'phone', 'images'] 
    
admin.site.register(Driver, DriverAdmin)
admin.site.register(models.Review)