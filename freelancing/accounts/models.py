from django.db import models
from django.contrib.auth.models import AbstractUser # type: ignore


# Create your models here.
class CustomUser(AbstractUser):
    pass

    # def get_seller(self):
    #     if(hasattr(self,'seller')):
    #         return self.seller
    #     return None
    
    # def get_buyer(self):
    #     if(hasattr(self,'buyer')):
    #         return self.buyer
    #     return None
    
    def role(self):
        if hasattr(self, 'seller'):
            return 'seller'
        elif hasattr(self, 'buyer'):
            return 'buyer'
        else:
            return None