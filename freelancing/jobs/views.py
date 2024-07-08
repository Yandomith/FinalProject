from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from jobs.models import Seller, Buyer, Job
from django.core.exceptions import PermissionDenied


class JobListView(ListView):
    model = Job
    template_name = 'jobs/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 10

class JobDetailView(DetailView):
    model = Job
    template_name = 'jobs/job_detail.html'
    # context_object_name = 'jobs'

    def get_object(self, queryset=None):
        code = self.kwargs.get("code")
        try:
            return Job.objects.get(code=code)
        except Job.DoesNotExist:
            raise Http404("Job not found")


class SellerListView(ListView):
    model = Seller

class SellerDetailView(DetailView):
    model = Seller

class SellerCreateView(CreateView):
    model = Seller
    fields = ['name', 'tagline', 'speciality', 'bio', 'website']
    success_url = reverse_lazy('job-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class BuyerCreateView(CreateView):
    model = Buyer
    fields = ['name', 'bio', 'location']
    success_url = reverse_lazy('job-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

@login_required
def handle_login(request):
    if hasattr(request.user, 'seller') or hasattr(request.user, 'buyer'):
        return redirect(reverse_lazy('job-list'))
    return render(request, 'jobs/choose_account.html')

class JobCreateView(CreateView):
    model = Job
    fields = ['title', 'budget', 'description', 'requirement']
    success_url = reverse_lazy('job-list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        if request.user.role() != 'Buyer':
            return HttpResponseForbidden("You do not have permission to post jobs.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.buyer = self.request.user.buyer
        return super().form_valid(form)
