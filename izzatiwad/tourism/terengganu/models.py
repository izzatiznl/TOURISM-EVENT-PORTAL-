# Create your models here.
from django.db import models

# Create your models here.
class Customer (models.Model):
    custid=models.AutoField(primary_key=True)
    custname=models.CharField(max_length=50)
    custphone=models.CharField(max_length=12)
    custmail=models.EmailField()
    password=models.CharField(max_length=50)
    username=models.CharField(max_length=50,null=True)


class Package(models.Model):
    packageid=models.AutoField( primary_key=True)
    packagename = models.CharField(max_length=100) 
    destinations = models.TextField()  
    tourdescription = models.TextField()  
    packageprice = models.FloatField()
    durationdays = models.IntegerField()  
    startdate = models.DateField() 
    enddate = models.DateField()
       
class Booking (models.Model):
    bookingid=models.AutoField(primary_key=True)
    custid=models.ForeignKey(Customer,on_delete=models.CASCADE)
    packageid=models.ForeignKey(Package,on_delete=models.CASCADE)
    bookingdate=models.DateField()
    bookingticket=models.IntegerField()
    totalprice=models.DecimalField(max_digits=10, decimal_places=2)

class Review (models.Model):
    custid=models.ForeignKey(Customer,on_delete=models.CASCADE)
    reviewcomment=models.TextField()