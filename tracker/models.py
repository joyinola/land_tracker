from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.conf import settings
# Create your models here.

def upload_doc(instance,filename):
    return f'land_tracker/{instance.user.user.fullname}/document/{filename}'


class UserManager(BaseUserManager):
    def create_user(self,email,phone_no,fullname,password=None,is_admin=False,**extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
  
        if phone_no is None:
            raise TypeError('Users should have a phone number')
        
        user=self.model(fullname=fullname,phone_no=phone_no,email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,phone_no,password=None,fullname='',email='',**extra_fields):
        
        
   
        if password is None:
            raise TypeError('Password must be provided ')
       
        user=self.create_user(email,phone_no,fullname,password,**extra_fields)
        user.is_superuser=True
        user.is_staff=True
        user.is_admin=True
        
        user.save()
        return user 

class User(AbstractBaseUser,PermissionsMixin):
    fullname=models.CharField(max_length=255,unique=False)
    email=models.EmailField(max_length=255,unique=True,null=True,blank=True,db_index=True)
    phone_no=models.CharField(max_length=255,unique=True)   
    is_verified=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    USERNAME_FIELD='phone_no'
    REQUIRED_FIELDS=[]

    objects=UserManager()

    def __str__(self):
        return f'{self.fullname} {self.phone_no}'

    def tokens(self):
        return ''

# class User(AbstractUser):
#     phone_no=models.CharField(max_length=20)
#     is_admin=models.BooleanField()

#     def __str__(self):
#         return self.username 


class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
   

class Admin(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    role=models.JSONField()


class Level(models.Model):
    stages=(
        ('stage 1','stage 1'),
        ('stage 2','stage 2'),
        ('stage 3','stage 3'),
        ('stage 4','stage 4'),
        ('stage 5','stage 5'),
        ('stage 6','stage 6'),
        ('stage 7','stage 7'),
        ('stage 8','stage 8'),
        ('stage 9','stage 9'),
        ('stage 10','stage 10'),
        ('stage 11','stage 11'),
        ('stage 12','stage 12'),
        ('stage 13','stage 13'),
        ('stage 14','stage 14'), 
        ('stage 15','stage 15'),
        ('stage 16','stage 16')
    )
    status=models.BooleanField(null=True,blank=True,default=False)
    updated_needed=models.BooleanField(null=True,blank=True,default=False)
    stage=models.CharField(choices=stages,max_length=68)
    feedback=models.CharField(max_length=255,null=True,blank=True)
    current_level=models.BooleanField(default=True)
    # application=models.ForeignKey(Application,on_delete=models.SET_NULL)

class Application(models.Model):

    purpose=(
        ('INDUSTRY','INDUSTRY'),
        ("COMMERCIAL","COMMERCIAL"),
    ("HOUSING ESTATE","HOUSING ESTATE")
    )
    level=models.ForeignKey(Level,on_delete=models.SET_NULL,null=True)
    user=models.ForeignKey(Customer,on_delete=models.CASCADE)
    age=models.IntegerField()
    birth_certificate=models.FileField(upload_to=upload_doc)
    nationality=models.CharField(max_length=255)
    state_of_origin=models.CharField(max_length=255)
    occupation=models.CharField(max_length=255)
    post_held=models.CharField(max_length=255)
    site_LGA=models.CharField(max_length=255)
    address=models.CharField(max_length=255)
    business_reg_cert=models.FileField(upload_to=upload_doc)
    business_reg_name=models.CharField(max_length=255)
    business_reg_num=models.CharField(max_length=255)
    business_reg_year=models.IntegerField()
    agent_name=models.CharField(max_length=255,null=True,blank=True)
    agent_address=models.CharField(max_length=255,null=True,blank=True)
    specific_purpose_of_land=models.TextField()
    plot_no=models.CharField(max_length=255)
    block_no=models.CharField(max_length=255)
    street_no=models.CharField(max_length=255)
    underdeveloped=models.BooleanField(default=False)
    minning=models.BooleanField(default=False)
    purpose_of_land=models.CharField(choices=purpose,max_length=68)
    development_proposal=models.FileField(upload_to=upload_doc,null=True,blank=True)
    amount=models.IntegerField()
    use=models.CharField(max_length=255)
    C_of_O=models.FileField(upload_to=upload_doc,null=True,blank=True) 
    reg_num=models.CharField(max_length=100,null=True,blank=True)

    
    




