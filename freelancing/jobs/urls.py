from django.urls import path
from .views import index,SellerListView, SellerDetailView,SellerCreateView,BuyerCreateView,handle_login


urlpatterns = [
    path('',SellerListView.as_view(), name='seller-list'),
    path('account-setup',handle_login, name='handle-login'),
    path('account-option',handle_login, name='account-option'),
    path('seller/<int:pk>/', SellerDetailView.as_view(), name= 'seller-detail'),
    path('seller/create/', SellerCreateView.as_view(), name='seller-create'),
    path('buyer/create/', BuyerCreateView.as_view(), name='buyer-create'),

]
