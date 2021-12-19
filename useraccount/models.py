from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.base import Model
from django.db.models.fields import BooleanField
from django.utils import timezone
from datetime import datetime



class MyAccountManager(BaseUserManager):
	def create_user(self, username, password=None,**kwargs):
		# if not email:
		# 	raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have an contact number')
            
        
		user = self.model(
            # email=self.normalize_email(email),**kwargs
			username=username,**kwargs
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, password):
		user = self.create_user(
			# email=self.normalize_email(email),
            username=username,
			password=password,
			#username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

class Account(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True ,null=True,blank=True)
    password = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    is_delivery = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_temporary = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    
    objects = MyAccountManager()
    
    def __str__(self):
        return self.username

	# For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
	    return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
	    return True

    def update_customer_account(self):
        self.is_customer = True
        self.is_temporary = False
        self.save()



class Deliveryperson(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    name    = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    emp_id  = models.CharField(max_length=50,null=True,blank=True,unique=True)
    contact_no = models.CharField(max_length=20,null=True,blank=True)
    bottle_assigned = models.CharField(max_length=20,null=True,blank=True,default=0)
    original_bottle_assigned = models.CharField(max_length=20,null=True,blank=True,default=0)
    address = models.CharField(max_length=1000,null=True,blank=True)
    location = models.CharField(max_length=500,null=True,blank=True)
    id_proof = models.CharField(max_length=500,null=True,blank=True)
    profile_img = models.ImageField(upload_to='deliveryboy/',null=True,blank=True)
    date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True ,null=True,blank=True)

    def __str__(self):
        return self.emp_id +" " +self.name

    def update_delivery_bottle(self,bottle_assigned):
        self.bottle_assigned = bottle_assigned
        self.save()

    def edit_delivery_account(self,original_bottle_assigned,bottle_assigned):
        self.original_bottle_assigned = original_bottle_assigned
        self.bottle_assigned = bottle_assigned
        self.save()



class Customer(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE,null=True,blank=True)
    delivery_boy = models.ForeignKey(Deliveryperson, on_delete=models.SET_NULL,null=True,blank=True)
    name    = models.CharField(max_length=100, null=True, blank=True)
    customer_id  = models.CharField(max_length=50,null=True,blank=True)
    email = models.EmailField(max_length=100,null=True,blank=True)
    contact_no = models.CharField(max_length=20,null=True,blank=True)
    bottle_numbers = models.CharField(max_length=20,null=True,blank=True,default=0)
    address = models.CharField(max_length=1000,null=True,blank=True)
    location = models.CharField(max_length=500,null=True,blank=True)
    id_proof = models.CharField(max_length=500,null=True,blank=True)
    profile_img = models.ImageField(upload_to='customerimg/',null=True,blank=True)
    sign_up_date = models.DateTimeField(verbose_name='sign_up_date', auto_now_add=True ,null=True,blank=True)
    request = models.BooleanField(default=False)

    money = models.CharField(max_length=50,null=True,blank=True,default=0)
    money_added_date = models.DateTimeField(verbose_name='money updated date', null=True,blank=True)


    def __str__(self):
        return self.name


    def update_request(self,obj):
        self.delivery_boy = obj
        self.request = True
        self.save()

    def update_bottle_details(self,bottle_numbers):
        self.bottle_numbers = bottle_numbers
        self.save()

    def update_money_date(self):
        self.money_added_date = timezone.now()
        self.save()

    def update_transaction_money(self,money):
        self.money = money
        self.save()


class Mainadmin(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    name    = models.CharField(max_length=100, null=True, blank=True)
    admin_id  = models.CharField(max_length=50,null=True,blank=True)
    email = models.EmailField(max_length=100,null=True,blank=True)
    contact_no = models.CharField(max_length=20,null=True,blank=True)
    address = models.CharField(max_length=1000,null=True,blank=True)
    location = models.CharField(max_length=500,null=True,blank=True)
    id_proof = models.CharField(max_length=500,null=True,blank=True)
    profile_img = models.ImageField(upload_to='adminimg/',null=True,blank=True)
    bottle_numbers = models.CharField(max_length=100,null=True,blank=True,default=0)
    assigned_bottle = models.CharField(max_length=100,null=True,blank=True,default=0)

    def __str__(self):
        return self.name

    def update_bottle_nos(self,bottle_numbers,assigned_bottle):
        self.bottle_numbers =bottle_numbers
        self.assigned_bottle = assigned_bottle
        self.save()



class Transcation(models.Model):
    connect_customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    delivery_per_name = models.CharField(max_length=100,null=True,blank=True)
    delivery_per_uid = models.CharField(max_length=100,null=True,blank=True)
    quantity = models.CharField(max_length=50, null=True, blank=True)
    price = models.CharField(max_length=50, null=True, blank=True)
    date_of_creation = models.DateTimeField(verbose_name='date of creation', auto_now_add=True)
    customer_approval = models.BooleanField(default=False)
    bottle_taken = models.BooleanField(default=False)
    bottle_nums = models.CharField(max_length=50, null=True, blank=True, default=0)
    remark = models.CharField(max_length=50, null=True, blank=True)
    customer_message = models.CharField(max_length=1000, null=True, blank=True)
    remark_date = models.DateTimeField(verbose_name='remark date',null=True,blank=True)
    final_approval = models.BooleanField(default=False)
    final_message = models.CharField(max_length=1000,null=True,blank=True)


    def __str__(self):
        return self.connect_customer.name

    def updateTransaction(self,remark,customer_message):
        self.customer_approval = True
        self.remark = remark
        self.customer_message = customer_message
        self.remark_date = datetime.now()
        self.save()

    def completeTransaction(self,final_message):
        self.final_approval = True
        self.final_message = final_message
        self.save()

    def update_transaction_bottle(self,bottle_nums):
        self.bottle_taken = False
        self.bottle_nums = bottle_nums
        self.save()

class moneyTransaction(models.Model):
    customer_obj = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    money_add = models.CharField(max_length=50,null=True,blank=True)
    transaction_type = models.CharField(max_length=100,null=True,blank=True)
    transaction_id = models.CharField(max_length=100,null=True,blank=True)
    transaction_registered_by = models.CharField(max_length=100,null=True,blank=True)
    added_date = models.DateTimeField(verbose_name='money added date', auto_now_add=True)
    remaining_amount = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.customer_obj.name +" " +str(self.added_date)

class MilkValue(models.Model):
    quantity = models.CharField(max_length=10,null=True,blank=True)
    price = models.CharField(max_length=10,null=True,blank=True)

    def __str__(self):
        return self.quantity


