from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Seller(models.Model):
    speciality_choices = [
        ('Computer systems manager','Computer systems manager'),
        ('Data analyst','Data analyst'),
        ('Data scientist','Data scientist'),
        ('Database administrator','Database administrator'),
        ('Digital marketing specialist','Digital marketing specialist'),
        ('Full stack developer','Full stack developer'),
        ('Graphic designer','Graphic designer'),
        ('IT consultant','IT consultant'),
        ('Network administrator','Network administrator'),
        ('Software engineer','Software engineer'),
        ('Web developer','Web developer'),
        ('Data analyst','Data analyst'),
        ('UX/UI designer','UX/UI designer'),
        ('Java developer','Java developer'),
        ('Python developer','Python developer'),
        ('Cybersecurity specialist','Cybersecurity specialist'),
        ('Artificial intelligence engineer','Artificial intelligence engineer'),
        ('Machine learning engineer','Machine learning engineer'),
        ('Help desk support specialist','Help desk support specialist'),
        ('Customer service representative','Customer service representative'),
        ('Salesforce developer','Salesforce developer'),
        ('Game Developer','Game Developer'),
        ('Animator','Animator'),
        ('3D modeler','3D modeler'),
        ('Video Editor','Video Editor'),
       ]
    owner = models.OneToOneField(User, on_delete= models.CASCADE)
    name= models.CharField(max_length=50)
    speciality= models.CharField (choices=speciality_choices, blank= False,max_length = 50 )
    tagline = models.CharField(max_length= 100)
    bio = models.TextField(blank=True)
    website = models.URLField(blank =True)

    def  __str__(self):
        return f"{self.id} | {self.name}"
    
class Buyer(models.Model):
    location = [
        ("Achham", "Achham"),
        ("Arghakhanchi", "Arghakhanchi"),
        ("Baglung", "Baglung"),
        ("Baitadi", "Baitadi"),
        ("Bajhang", "Bajhang"),
        ("Bajura", "Bajura"),
        ("Banke", "Banke"),
        ("Bara", "Bara"),
        ("Bardiya", "Bardiya"),
        ("Bhaktapur", "Bhaktapur"),
        ("Bhojpur", "Bhojpur"),
        ("Chitwan", "Chitwan"),
        ("Dadeldhura", "Dadeldhura"),
        ("Dailekh", "Dailekh"),
        ("Dang", "Dang"),
        ("Darchula", "Darchula"),
        ("Dhading", "Dhading"),
        ("Dhankuta", "Dhankuta"),
        ("Dhanusha", "Dhanusha"),
        ("Dolakha", "Dolakha"),
        ("Dolpa", "Dolpa"),
        ("Doti", "Doti"),
        ("Eastern Rukum", "Eastern Rukum"),
        ("Gorkha", "Gorkha"),
        ("Gulmi", "Gulmi"),
        ("Humla", "Humla"),
        ("Ilam", "Ilam"),
        ("Jajarkot", "Jajarkot"),
        ("Jhapa", "Jhapa"),
        ("Jumla", "Jumla"),
        ("Kailali", "Kailali"),
        ("Kalikot", "Kalikot"),
        ("Kanchanpur", "Kanchanpur"),
        ("Kapilvastu", "Kapilvastu"),
        ("Kaski", "Kaski"),
        ("Kathmandu", "Kathmandu"),
        ("Kavrepalanchok", "Kavrepalanchok"),
        ("Khotang", "Khotang"),
        ("Lalitpur", "Lalitpur"),
        ("Lamjung", "Lamjung"),
        ("Mahottari", "Mahottari"),
        ("Makwanpur", "Makwanpur"),
        ("Manang", "Manang"),
        ("Morang", "Morang"),
        ("Mugu", "Mugu"),
        ("Mustang", "Mustang"),
        ("Myagdi", "Myagdi"),
        ("Nawalpur", "Nawalpur"),
        ("Nuwakot", "Nuwakot"),
        ("Okhaldhunga", "Okhaldhunga"),
        ("Palpa", "Palpa"),
        ("Panchthar", "Panchthar"),
        ("Parbat", "Parbat"),
        ("Parsa", "Parsa"),
        ("Pyuthan", "Pyuthan"),
        ("Ramechhap", "Ramechhap"),
        ("Rasuwa", "Rasuwa"),
        ("Rautahat", "Rautahat"),
        ("Rolpa", "Rolpa"),
        ("Rupandehi", "Rupandehi"),
        ("Salyan", "Salyan"),
        ("Sankhuwasabha", "Sankhuwasabha"),
        ("Saptari", "Saptari"),
        ("Sarlahi", "Sarlahi"),
        ("Sindhuli", "Sindhuli"),
        ("Sindhupalchok", "Sindhupalchok"),
        ("Siraha", "Siraha"),
        ("Solukhumbu", "Solukhumbu"),
        ("Sunsari", "Sunsari"),
        ("Surkhet", "Surkhet"),
        ("Syangja", "Syangja"),
        ("Tanahun", "Tanahun"),
        ("Taplejung", "Taplejung"),
        ("Tehrathum", "Tehrathum"),
        ("Udayapur", "Udayapur"),
        ("Western Rukum", "Western Rukum"),
    ]

    owner = models.OneToOneField(User, on_delete= models.CASCADE)
    name= models.CharField(max_length=50)
    bio = models.TextField(blank=True)
    location = models.CharField(choices= location, blank= False , max_length=100)
    
    def  __str__(self):
        return f"{self.id} | {self.name}"

import uuid

class Job(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.TextField()
    budget = models.IntegerField()
    description = models.TextField()
    requirement = models.CharField(max_length=1000)
    code = models.CharField(max_length=10, unique=True, blank=True)  # Add a new field for the unique code

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()
        super(Job, self).save(*args, **kwargs)

    def generate_unique_code(self):
        return str(uuid.uuid4())[:10]  # Generate a unique code, you can customize the length and format

    def __str__(self):
        return f"{self.id} | {self.title}"



    