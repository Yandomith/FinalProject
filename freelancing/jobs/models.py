import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from jobs.choices import SPECIALITY_CHOICES,LOCATION_CHOICES

User = get_user_model()

# Create your models here.
class Seller(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    profile_pic = models.ImageField(upload_to="profile/")
    speciality = models.CharField(choices=SPECIALITY_CHOICES, max_length=50)
    tagline = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return f"{self.id} | {self.name}"

class Buyer(models.Model):
  
    owner = models.OneToOneField(User, on_delete=models.CASCADE, )
    name = models.CharField(max_length=50)
    profile_pic = models.ImageField(upload_to="profile/")
    bio = models.TextField(blank=True)
    location = models.CharField(choices=LOCATION_CHOICES, max_length=100)

    def __str__(self):
        return f"{self.id} | {self.name}"

class Job(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    budget = models.IntegerField(validators=[MinValueValidator(1000)])   
    description = models.TextField()
    requirement = models.TextField()
    expertise_required = models.CharField(choices=SPECIALITY_CHOICES, max_length=50, default="None" )
    timestamp = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=10, unique=True, primary_key=True,)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()
        super(Job, self).save(*args, **kwargs)

    def generate_unique_code(self): 
        return str(uuid.uuid4())[:10]

    def __str__(self):
        return f"{self.id} | {self.title}"

class ApplyJob(models.Model):
    status_choices=(
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Pending', 'Pending')
    )
    user = models.ForeignKey(User , on_delete= models.CASCADE )
    Job = models.ForeignKey(Job, on_delete= models.CASCADE,to_field='code')
    coverLetter = models.TextField(max_length=500, blank=False)
    priceRange=models.PositiveIntegerField( blank=False )
    timestamp= models.DateTimeField(auto_now_add=True)
    status= models.CharField(max_length=10, choices=status_choices)