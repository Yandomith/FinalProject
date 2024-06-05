from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, DetailView

from jobs.models import Seller

def index(request):
    return HttpResponse("hehe")


class SellerListView(ListView):
    model= Seller

class SellerDetailView(DetailView):
    model = Seller