from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Person(models.Model):
    city=models.CharField(max_length=100,null=True,default='')
    date=models.DateTimeField(auto_now_add=True)

class Product(models.Model):
    name=models.CharField(max_length=10)
    price = models.IntegerField()
    image = models.ImageField(upload_to = 'products', default='')

    def __str__(self):
        return self.name

class Cart(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField()
    userid=models.CharField(max_length=100,default='')


class Country(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Address(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    address= models.CharField(max_length=200)
    pincode = models.CharField(max_length=6)
    mobile_no = models.CharField(max_length=10)
    user_id=models.IntegerField(default='')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.first_name
    
class Order(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField()
    userid = models.IntegerField()
    created_at = models.DateTimeField()
    stripe_payment_intent = models.CharField(max_length=2000)
    email=models.EmailField()
    has_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=10)
    address = models.ForeignKey(Address,on_delete=models.CASCADE,null=True)


