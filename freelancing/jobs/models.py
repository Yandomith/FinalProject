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
    

class Buyer (models.Model):
    owner = models.OneToOneField(User, on_delete= models.CASCADE)
    name= models.CharField(max_length=50)
    bio = models.TextField(blank=True)
    
    def  __str__(self):
        return f"{self.id} | {self.name}"


    