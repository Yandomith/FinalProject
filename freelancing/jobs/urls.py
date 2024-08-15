from django.urls import path
from .views import SellerListView, SellerDetailView,SellerCreateView,BuyerCreateView,handle_login,JobDetailView,JobCreateView,JobListView,JobUpdateView,ApplyJobCreateView,my_jobs,delete_job, home


urlpatterns = [
     path("", home, name="index"),
    path('sellers',SellerListView.as_view(), name='seller-list'),
    path('account-setup',handle_login, name='handle-login'),
    path('seller/<int:pk>/', SellerDetailView.as_view(), name= 'seller-detail'),
    path('seller/create/', SellerCreateView.as_view(), name='seller-create'),
    path('buyer/create/', BuyerCreateView.as_view(), name='buyer-create'),
    path('job/create/', JobCreateView.as_view(), name='job-create'),
    path('find-work/',JobListView.as_view(), name='job-list'),
    path('job/<str:code>/',JobDetailView.as_view(), name='job-detail'),
    path('job/update/<str:code>/',JobUpdateView.as_view(), name='job-update'),
    path('job/<str:code>/apply/', ApplyJobCreateView.as_view(), name='apply-job'),
    path('my-jobs/', my_jobs, name='my_jobs'),
    path('delete-job/<str:job_code>/', delete_job, name='job-delete'),

]
    