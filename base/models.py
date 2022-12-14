from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.



class MyAccountManager(BaseUserManager):
    def create_user(self, full_name, email, password=None):
        if not email:
            raise ValueError('Email Required')
        if not full_name:
            raise ValueError('Full Name Required')
        user = self.model(
            email = self.normalize_email(email),
            full_name = full_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,full_name, email, password):
        user = self.create_user( 
            email = self.normalize_email(email),
            full_name = full_name,
            password = password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    class UserType(models.TextChoices):
        OWNER           = 'Owner'
        DEALER          = 'Dealer'

    username = None
    full_name           = models.CharField(max_length=50)   
    email               = models.EmailField(max_length=100, unique=True)
    phone_number        = models.CharField(max_length=50)
    profile             = models.ImageField(upload_to='photo/user_profile')
    city                = models.CharField(max_length=100)
    user_type           = models.CharField(max_length=30, choices=UserType.choices, null=True, blank=True)

    # required
    date_joined         = models.DateTimeField(auto_now_add=True)
    last_login          = models.DateTimeField(auto_now_add=True)
    is_admin            = models.BooleanField(default=False)
    is_staff            = models.BooleanField(default=False)
    is_active           = models.BooleanField(default=True)
    is_superadmin       = models.BooleanField(default=False)

    USERNAME_FIELD      = 'email'
    REQUIRED_FIELDS     = ['full_name']


    objects = MyAccountManager()

    def __str__(self):
        return self.email
        
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True