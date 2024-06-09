from django.urls import path
from .views import index,SellerListView, SellerDetailView


urlpatterns = [
    path('',SellerListView.as_view(), name='seller-list'),
    path('seller/<int:pk>/', SellerDetailView.as_view(), name= 'seller-detail'),

]
