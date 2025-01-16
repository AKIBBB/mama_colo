from django.db import models
from django.contrib.auth.models import User
from customer.models import Customer
# Create your models here.
class Driver(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    images=models.ImageField(upload_to='driver/images/')
    rent=models.IntegerField()
    email=models.EmailField()
    phone=models.TextField()
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
STAR_CHOICES=[
    ('⭐' , '⭐'),
    ('⭐⭐','⭐⭐'),
    ('⭐⭐⭐','⭐⭐⭐'),
    ('⭐⭐⭐⭐','⭐⭐⭐⭐'),
    ('⭐⭐⭐⭐⭐','⭐⭐⭐⭐⭐'),
]
class Review(models.Model):
    reviewer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    driver=models.ForeignKey(Driver,on_delete=models.CASCADE)
    body=models.TextField()
    crated=models.DateTimeField(auto_now_add=True)
    rating=models.CharField(choices=STAR_CHOICES,max_length=15)
       
    def __str__(self):
        return f"Customer:{self.reviewer.user.last_name}; Driver:{self.driver.user.last_name}"