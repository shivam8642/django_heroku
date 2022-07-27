
from ast import Add
from django.contrib import admin
from .models import Product,Cart,Person,Order,Country,City,Address
# Register your models here.
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Order)
admin.site.register(Person)
admin.site.register(Address)
