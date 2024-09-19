from django.urls import path
from .views import SellerListView, SellerDetailView,SellerCreateView,BuyerCreateView,BuyerDetailView,handle_login,JobDetailView,JobCreateView,JobListView,JobUpdateView,ApplyJobCreateView,my_jobs,delete_job, home,all_applicants, notifications_view, mark_notifications_as_read ,SellerProfileUpdateView,BuyerProfileUpdateView, my_proposalsListView,chat_thread , user_list



# ,inbox,sent_messages,compose_message
urlpatterns = [
    path("", home, name="index"),
     path('seller/profile/<int:pk>/', SellerProfileUpdateView.as_view(), name='seller_editprofile'),
    path('buyer/profile/<int:pk>/', BuyerProfileUpdateView.as_view(), name='buyer_editprofile'),


    path('sellers',SellerListView.as_view(), name='seller-list'),
    path('account-setup',handle_login, name='handle-login'),
    path('seller/<int:pk>/', SellerDetailView.as_view(), name= 'seller-detail'),
    path('buyer/<int:pk>/', BuyerDetailView.as_view(), name= 'buyer-detail'),

    path('seller/create/', SellerCreateView.as_view(), name='seller-create'),
    path('buyer/create/', BuyerCreateView.as_view(), name='buyer-create'),
    path('job/create/', JobCreateView.as_view(), name='job-create'),
    path('find-work/',JobListView.as_view(), name='job-list'),
    path('job/<str:code>/',JobDetailView.as_view(), name='job-detail'),
    path('job/update/<str:code>/',JobUpdateView.as_view(), name='job-update'),
    path('job/<str:code>/apply/', ApplyJobCreateView.as_view(), name='apply-job'),
    path('my-jobs/', my_jobs, name='my_jobs'),
    path('my-proposals/', my_proposalsListView.as_view(), name='my-proposals'),

    path('delete-job/<str:job_code>/', delete_job, name='job-delete'),
    path('applicants/<str:code>', all_applicants, name='all_applicants'),

    path('notifications/', notifications_view, name='notifications'),
    path('notifications/mark-as-read/', mark_notifications_as_read,name='mark-notifications-as-read'),

    path('chat/<int:pk>/', chat_thread, name='chat_thread'),
    path('conversations/', user_list, name='conversations'),
]
    