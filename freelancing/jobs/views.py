from django.forms import BaseModelForm
from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, DetailView,CreateView
from django.urls import reverse_lazy

from jobs.models import Seller, Buyer

def index(request):
    return HttpResponse("hehe")


class SellerListView(ListView):
    model= Seller

class SellerDetailView(DetailView):
    model = Seller

class SellerCreateView(CreateView):
    model = Seller
    fields = ['name', 'tagline','bio','website']
    success_url = reverse_lazy('Seller-list')

    def form_valid(self, form):
        form.instance.owner =self.request.user
        return super(SellerCreateView,self).form_valid(form)
    
class BuyerCreateView(CreateView):
    model = Buyer
    fields = ['name','bio']
    success_url = reverse_lazy('Seller-list')

    def form_valid(self, form):
        form.instance.owner =self.request.user
        return super(SellerCreateView,self).form_valid(form)