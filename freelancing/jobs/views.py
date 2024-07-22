from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView,UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from jobs.models import Seller, Buyer, Job,ApplyJob
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin


class JobListView(ListView):
    model = Job
    template_name = 'jobs/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['speciality_choices'] = Seller.SPECIALITY_CHOICES
        context['location_choices'] = Buyer.LOCATION_CHOICES
        return context
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Job.objects.filter(title__icontains=query)  # Adjust fields as needed
        return Job.objects.all()

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


class JobUpdateView(UpdateView):
    model = Job
    fields = ['title', 'budget', 'description', 'requirement']
    success_url = reverse_lazy('job-list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        if request.user.role() != 'Buyer':
            return HttpResponseForbidden("You do not have permission to post jobs.")
        
        job = get_object_or_404(Job, code=kwargs['code'])
        if job.buyer != request.user.buyer:
            return HttpResponseForbidden("You do not have permission to edit this job.")
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        # Fetch the Job object using the unique code
        return get_object_or_404(Job, code=self.kwargs['code'])
    def form_valid(self, form):
        return super().form_valid(form)
    

class ApplyJobCreateView(LoginRequiredMixin, CreateView):
    model = ApplyJob
    fields = []  # Adjust fields as necessary
    template_name = 'jobs/applyjob_form.html'
    success_url = reverse_lazy('job-list')  # Adjust as necessary

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        # Check if user is a seller
        if not hasattr(request.user, 'seller'):
            return HttpResponseForbidden("You must be a seller to apply for jobs.")

        # Get the job based on the code from the URL
        self.job = get_object_or_404(Job, code=kwargs['code'])

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Set the job and user fields
        form.instance.user = self.request.user
        form.instance.Job = self.job
        return super().form_valid(form) 