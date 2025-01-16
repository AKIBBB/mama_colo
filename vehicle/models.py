from django.db import models
from customer.models import Customer
from driver.models import Driver


# Create your models here.
class RiderRequest(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    status=[
        ('Completed','Complete'),
        ('Pending','Pending'),
        ('Running', 'Running'),
    ]
    car_types=[
        ('Car','Car'),
        ('Taxi','Taxi'),
        ('Bike','Bike'),
    ]
    status=models.CharField(choices=status,max_length=20)
    types=models.CharField(choices=car_types,max_length=20)
    address = models.CharField(max_length=50)
    geolocation =models.CharField(max_length=50)
    cancel=models.BooleanField(default=False)
    
    
    def __str__(self):
        return f"Driver : {self.driver.user.first_name} , Customer: {self.driver.user.first_name}"
    
    
    
class Vehicle(models.Model):
    drive=models.ForeignKey(Driver,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='driver/images')
    registration_number = models.CharField(max_length=20)
    vehicle_model = models.CharField(max_length=50)