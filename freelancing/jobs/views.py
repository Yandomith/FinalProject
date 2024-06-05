from django.shortcuts import render, HttpResponse
from django.views.generic import ListView

from jobs.models import Seller

def index(request):
    return HttpResponse("hehe")


class SellerListView(ListView):
    model= Seller