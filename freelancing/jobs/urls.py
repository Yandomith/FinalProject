from django.urls import path
from .views import SellerListView, SellerDetailView,SellerCreateView,BuyerCreateView,handle_login,JobDetailView,JobCreateView,JobListView


urlpatterns = [
    path('',SellerListView.as_view(), name='seller-list'),
    path('account-setup',handle_login, name='handle-login'),
    path('seller/<int:pk>/', SellerDetailView.as_view(), name= 'seller-detail'),
    path('seller/create/', SellerCreateView.as_view(), name='seller-create'),
    path('buyer/create/', BuyerCreateView.as_view(), name='buyer-create'),
    path('job/create/', JobCreateView.as_view(), name='job-create'),
    path('find-work/',JobListView.as_view(), name='job-list'),
    path('job/<str:code>/',JobDetailView.as_view(), name='job-detail'),

]
 