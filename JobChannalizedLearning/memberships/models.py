from django.db import models
from user_account.models import User

# Create your models here.
class Membership(models.Model):

    membership_choices = [
        ('Premium','Premium'),
        ('Vip','Vip')
    ]

    membership = models.CharField(choices=membership_choices,max_length=20,blank=True)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)


