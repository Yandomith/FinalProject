from django.contrib import admin
from .models import Seller, Buyer,Job

# Register your models here.

admin.site.register(Seller)
admin.site.register(Buyer)
admin.site.register(Job)

