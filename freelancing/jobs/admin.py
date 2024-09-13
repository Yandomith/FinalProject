from django.contrib import admin
from .models import Seller, Buyer,Job,ApplyJob


class JobAdmin(admin.ModelAdmin):
    list_display = ('code', 'title','buyer', 'budget', 'timestamp', 'expertise_required')
    search_fields = ('code', 'title')

class SellerAdmin(admin.ModelAdmin):
    list_display = ('id','owner','name', 'speciality', 'tagline' , 'website' )
    search_fields = ('id','name')

class BuyerAdmin(admin.ModelAdmin):
    list_display= ('id', 'owner', 'name', 'location')
    search_fields = ('id', 'name')
    


admin.site.register(Seller,SellerAdmin)
admin.site.register(Buyer, BuyerAdmin)
admin.site.register(Job,JobAdmin)
admin.site.register(ApplyJob)
