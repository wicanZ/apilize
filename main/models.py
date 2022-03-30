from django.db import models
from django.forms import CharField, ImageField
import uuid
# Create your models here.
# model store in db-sqlite
# for user model we need
# from django.contrib.auth.models import UserManager
# from django.contrib.auth.models import User


from django.contrib.auth.models import AbstractUser ,AbstractBaseUser ,BaseUserManager ,PermissionsMixin


# modifies super user 
class UserManager( BaseUserManager ):
    def create_user(self, email , password = None ):
        if not email :
            raise ValueError('Email is Required!')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self , email , password ) : # instance object inheritance just like abstract or interface in java
        if password is None :
            raise ValueError("Password Needed")
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

# create user 
class User( AbstractBaseUser , PermissionsMixin ) :
    id = models.UUIDField(primary_key=True , default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True , verbose_name='Email Address', )
    password = models.CharField(max_length=100)
    username = None
    is_active = models.BooleanField(default=True)
    is_staff  =  models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIED_FIELDS = []
    objects = UserManager()
    def __str__(self):
        return self.email
    # UserApi._meta.get_field_by_name('email')[0]._unique=True
    class Meta:
        db_table = 'user'


class UserProfile( models.Model ):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50, unique=False)
    last_name = models.CharField(max_length=50, unique=False)
    # address  = models.CharField(max_length=100, null=False, blank=False)
    phone_number = models.CharField(max_length=10, unique=True, null=False, blank=False)
    age = models.PositiveIntegerField(null=False, blank=False)

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self) -> str:
        return self.first_name 

    class Meta:
        db_table = "Userprofile"

# class IP( models.Model ) :
#     id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False )
#     ip =  models.GenericIPAddressField()


class TypesBikes(models.Model ) :
    id        = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # = models.ForeignKey( Items , on_delete=models.CASCADE)
    biketypes = models.CharField( max_length= 100 )
    created   = models.DateTimeField( auto_now_add=True )
    updated   = models.DateTimeField( auto_now=True )

    def __str__(self):
        return self.biketypes

    class Meta:
        ordering = ['-created']


class BikeDetails( models.Model ) :
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tybikes    = models.ForeignKey( TypesBikes ,on_delete=models.CASCADE)
    cyclename = models.CharField(max_length=100)
    image = models.ImageField( upload_to ="image_cycle/" , null=False  , max_length=100)
    # specs = models.FileField(db_index=True , upload_to="specs")
    descriptive = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    likes  = models.ManyToManyField( User , related_name='bikename')
    #views  = models.ManyToManyField( IP , related_name='ipaddr')
    
    def __str__(self) -> str:
        form = "{}:{}".format(self.cyclename, self.price)
        return form


class Accessories( models.Model ) :
    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False )
    name =  models.CharField(max_length=100)
    image = models.ImageField( upload_to ="imageaccesories/" , null=False  , max_length=100)
    # specs = models.FileField(db_index=True , upload_to="specs")
    descriptive = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    likes  = models.ManyToManyField( User , related_name='accname')

    def __str__( self ) :
        return self.name 



#class Payment( models.Model ) :
#class PaymentDetails( models.Model ) :


