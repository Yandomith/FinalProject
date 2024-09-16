from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView,UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden,HttpResponse

from jobs.models import Seller, Buyer, Job,ApplyJob,Notification, User
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from .forms import JobForm
from .choices import SPECIALITY_CHOICES , LOCATION_CHOICES



class SellerCreateView(CreateView):
    model = Seller
    fields = ['name','profile_pic', 'tagline', 'speciality', 'bio', 'website']
    success_url = reverse_lazy('account_login')

    def form_valid(self, form,):
        create_notification(self.request.user, "You have logged in as a Seller !")

        form.instance.owner = self.request.user
        return super().form_valid(form)


class BuyerCreateView(CreateView):
    model = Buyer
    fields = ['name','profile_pic', 'bio', 'location']
    success_url = reverse_lazy('account_login')

    def form_valid(self, form, ):
        create_notification(self.request.user, "You Deleted a Job !")
        form.instance.owner = self.request.user
        return super().form_valid(form)



@login_required
def handle_login(request):
    if hasattr(request.user, 'seller') or hasattr(request.user, 'buyer'):
        return redirect(reverse_lazy('job-list'))
    return render(request, 'jobs/choose_account.html')


def home (request):
    if not request.user.is_authenticated:
        return render (request, 'jobs/home.html')
    else:
        return redirect(reverse_lazy('job-list'))






class SellerListView(ListView):
    model = Seller









class SellerDetailView(DetailView):
    model = Seller
    template_name = 'jobs/seller_detail.html'
    context_object_name = 'seller'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seller = self.object
        try:
            proposals = ApplyJob.objects.filter(user=seller.owner.id)
        except ApplyJob.DoesNotExist:
            proposals =[]

        context['owner_id'] = seller.owner.id
        context['proposals'] = proposals
        return context

class BuyerDetailView(DetailView):
    model = Buyer
    template_name = 'jobs/buyer_detail.html'
    context_object_name = 'buyer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        buyer = self.object

        try:
            jobs = Job.objects.filter(buyer=buyer)
        except Job.DoesNotExist:
            jobs = []

        context['owner_id'] = buyer.owner.id
        context['jobs'] = jobs 
        return context
    

















class BuyerProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Buyer
    template_name = 'jobs/profile_edit.html'
    success_url = reverse_lazy('job-list')
    fields = ['name','profile_pic', 'bio', 'location' ]

    def get_object(self, queryset=None):
        create_notification(self.request.user, "You have updated your profile !")
        return get_object_or_404(Buyer, pk=self.kwargs.get('pk'))

class SellerProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Seller
    template_name = 'jobs/profile_edit.html'
    success_url = reverse_lazy('job-list')
    fields = ['name','profile_pic','tagline','bio','website']

    def get_object(self, queryset=None):
        create_notification(self.request.user, "You have updated your profile !")
        return get_object_or_404(Seller, pk=self.kwargs.get('pk'))



















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
        create_notification(self.request.user, f" You have Created the job")
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
        job = Job.objects.get(code=self.kwargs['code'])
        create_notification(self.request.user, f" You have updated the job: {job.title}")

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

        if query:
            job_queryset = Job.objects.filter(title__icontains=query)
        elif location:
            job_queryset = Job.objects.filter(buyer__location=location)
        else:
            job_queryset = Job.objects.all()

        context['speciality_choices'] = SPECIALITY_CHOICES
        context['location_choices'] = LOCATION_CHOICES

        applied_jobs = ApplyJob.objects.filter(user=self.request.user).values_list('Job__code', flat=True)


        for job in job_queryset:
            job.has_applied = job.code in applied_jobs
        
        context['jobs'] = job_queryset 
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




class my_proposalsListView(ListView):
    model = ApplyJob
    template_name = 'jobs/proposals.html'
    context_object_name = 'proposals'

    def get_queryset(self):
        seller = self.request.user.id
        return ApplyJob.objects.filter(user=seller)















@login_required
def delete_job(request, job_code):
    job = get_object_or_404(Job, code=job_code)
    buyer = Buyer.objects.get(owner=request.user)
    
    if job.buyer != buyer:
        return HttpResponseForbidden("You are not allowed to delete this job.")

    job.delete()
    create_notification(request.user, "You Deleted a Job !")
    return redirect('my_jobs')


class ApplyJobCreateView(LoginRequiredMixin, CreateView):
    model = ApplyJob
    fields = ['coverLetter','priceRange']  # Adjust fields as necessary
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
        job = Job.objects.get(code=self.kwargs['code'])
    
        create_notification(job.buyer.owner, f"New application for your job: {job.title}")
        create_notification(self.request.user, f" You have applied for the job: {job.title}")

        form.instance.user = self.request.user
        form.instance.Job = self.job
        return super().form_valid(form) 
    

def all_applicants(request, *args, **kwargs):
    code = kwargs.get('code')
    job = get_object_or_404(Job, code=code)
    applicants = job.applyjob_set.all()
    context = {'job': job, 'applicants': applicants}
    return render(request, 'jobs/all_applicants.html', context)





    
def create_notification(user, message):
    Notification.objects.create(user=user, message=message)

def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user,)
    context = {'notifications': notifications}
    if notifications:
        mark_notifications_as_read(request)

    return render(request, 'jobs/notifications.html', context)

def mark_notifications_as_read(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    notifications.update(is_read=True)


