from django.forms import BaseModelForm
from django.shortcuts import render, HttpResponse,redirect
from django.views.generic import ListView, DetailView,CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from jobs.models import Seller, Buyer

def index(request):
    return HttpResponse("hehe")


class SellerListView(ListView):
    model= Seller

class SellerDetailView(DetailView):
    model = Seller

class SellerCreateView(CreateView):
    model = Seller
    fields = ['name', 'tagline','speciality','bio','website']
    success_url = reverse_lazy('seller-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
class BuyerCreateView(CreateView):
    model = Buyer
    fields = ['name','bio']
    success_url = reverse_lazy('seller-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
@login_required
def handle_login(request):
    #check if has account 
    if request.user.get_seller() or request.user.get_buyer():
        return redirect(reverse_lazy('seller-list'))
    return render (request,'jobs/choose_account.html',{})
