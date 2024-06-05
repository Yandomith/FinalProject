from django.urls import path
from .views import index,SellerListView


urlpatterns = [
    path('',SellerListView.as_view(), name='home'),

]
