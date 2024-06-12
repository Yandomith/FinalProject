from django.urls import path
from .views import index,SellerListView, SellerDetailView,SellerCreateView,BuyerCreateView


urlpatterns = [
    path('',SellerListView.as_view(), name='seller-list'),
    path('seller/<int:pk>/', SellerDetailView.as_view(), name= 'seller-detail'),
    path('seller/create', SellerCreateView.as_view(), name='seller-createForm'),
    path('buyer/create', BuyerCreateView.as_view(), name='buyer-createForm'),

]
