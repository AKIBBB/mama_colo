from django.contrib import admin
from .models import ContactUs
# Register your models here.
class ContactUsModelAdmin(admin.ModelAdmin):
    list_display=['id','name','phone','email','opinion']
admin.site.register(ContactUs,ContactUsModelAdmin)