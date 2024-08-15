from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView,UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden,HttpResponse
from jobs.models import Seller, Buyer, Job,ApplyJob
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from .forms import JobForm
from .choices import SPECIALITY_CHOICES , LOCATION_CHOICES


class SellerCreateView(CreateView):
    model = Seller
    fields = ['name','profile_pic', 'tagline', 'speciality', 'bio', 'website']
    success_url = reverse_lazy('account_login')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class BuyerCreateView(CreateView):
    model = Buyer
    fields = ['name','profile_pic', 'bio', 'location']
    success_url = reverse_lazy('account_login')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

@login_required
def handle_login(request):
    if hasattr(request.user, 'seller') or hasattr(request.user, 'buyer'):
        return redirect(reverse_lazy('job-list'))
    return render(request, 'jobs/choose_account.html')

def home (request):
    return render (request, 'jobs/home.html')

class SellerListView(ListView):
    model = Seller

class SellerDetailView(DetailView):
    model = Seller


class JobCreateView(CreateView):
    model = Job
    form_class = JobForm
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
    

class JobListView(LoginRequiredMixin,ListView):
    model = Job
    template_name = 'jobs/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 5
    login_url = 'handle-login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        location = self.request.GET.get('location')

        # Filter jobs based on query and location
        if query:
            job_queryset = Job.objects.filter(title__icontains=query)
        elif location:
            job_queryset = Job.objects.filter(buyer__location=location)
        else:
            job_queryset = Job.objects.all()

        # Pass choices and job count to context
        context['speciality_choices'] = SPECIALITY_CHOICES
        context['location_choices'] = LOCATION_CHOICES

        applied_jobs = ApplyJob.objects.filter(user=self.request.user).values_list('Job__code', flat=True)

        # Add application status to each job
        for job in job_queryset:
            job.has_applied = job.code in applied_jobs
        
        context['jobs'] = job_queryset  # Update context with filtered job queryset
        return context


    def get_queryset(self):
        query = self.request.GET.get('q')
        location = self.request.GET.get('location')

        queryset = Job.objects.all()
        if query:
            queryset = queryset.filter(title__icontains=query)
        if location:
            queryset = queryset.filter(buyer__location=location)

        return queryset.order_by('-timestamp')


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
        
def my_jobs(request):
    try:
        buyer = Buyer.objects.get(owner=request.user)
        jobs = Job.objects.filter(buyer=buyer)
    except Buyer.DoesNotExist:
        jobs = []
    return render(request, 'jobs/my_jobs.html', {'jobs': jobs})

@login_required
def delete_job(request, job_code):
    job = get_object_or_404(Job, code=job_code)
    buyer = Buyer.objects.get(owner=request.user)
    
    if job.buyer != buyer:
        return HttpResponseForbidden("You are not allowed to delete this job.")

    job.delete()
    return redirect('my_jobs')


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
        
        if ApplyJob.objects.filter(user=request.user, Job = kwargs['code']).exists():
           return HttpResponse("you have applied to this job already")
        
        self.job = get_object_or_404(Job, code=kwargs['code'])

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Set the job and user fields
        form.instance.user = self.request.user
        form.instance.Job = self.job
        return super().form_valid(form) 