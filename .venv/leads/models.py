from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
import datetime
#for authentication: gives a class authentication powers


# Create your models here.
#creation of database table
class User(AbstractUser):
    id = models.BigAutoField(primary_key = True)
    is_organisor = models.BooleanField(default = True)
    is_agent = models.BooleanField(default = False)

class UserProfile(models.Model):
    id = models.BigAutoField(primary_key = True)
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user = instance)

def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

# Lead
class Lead(models.Model):    
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    contact_info = models.TextField()
    age = models.IntegerField(default = 0)
    description = models.TextField()
    organisation = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
    email = models.EmailField()
    agent = models.ForeignKey("Agent", null = True, blank= True, on_delete = models.SET_NULL)
    category = models.ForeignKey("Category", related_name="leads", null = True, blank= True, on_delete= models.SET_NULL)
    date_added = models.DateTimeField(auto_now_add=True)
    converted_date = models.DateTimeField(null=True, blank=True)

    #if CASCADE, agent is deleted, lead is deleted
    #if SET_NULL, lead is null
    #if SET_DEFAULT, lead is set to default

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete = models.CASCADE)

    def __str__(self):
        return self.user.first_name

class Category(models.Model):
    name = models.CharField(max_length = 30) #New, Contacted, Converted, Unconverted
    organisation = models.ForeignKey(UserProfile, on_delete = models.CASCADE)

    def __str__(self):
        return self.name

class Product(models.Model):
    PRODUCT_CHOICES = (
        ('Electronic Appliances','Electronic Appliances'),
        ('Skincare', 'Skincare'),
        ('Kitchen & Dining', 'Kitchen & Dining'),
        ('Toys', "Toys"),
        ('Mobile Accessories', 'Mobile Accessories'),
        ('Groceries', 'Groceries'),
    )
    name = models.CharField(max_length = 300)
    description = models.TextField()
    unit_price = models.DecimalField(max_digits = 10, decimal_places = 2)
    product_category = models.CharField(max_length=50, choices = PRODUCT_CHOICES)

    def __str__(self):
        return self.name
    
class Purchase(models.Model):
    PAYMENT_CHOICES = (
        ('Credit/Debit','Credit/Debit'),
        ('Cash','Cash'),
        ('Grab Paylater', 'Grab Paylater'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Reward Points', 'Reward Points'),
        ('PayPal', 'PayPal'),
    )

    lead = models.ForeignKey("Lead", on_delete = models.CASCADE, blank= True, null = True)
    product = models.ForeignKey("Product", on_delete = models.CASCADE, blank = True, null = True)
    agent = models.ForeignKey("Agent",on_delete = models.CASCADE, blank = True, null = True)
    payment_method = models.CharField(choices = PAYMENT_CHOICES, max_length = 100)
    purchase_date = models.DateTimeField(auto_now_add= True)
    quantity = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits = 10, decimal_places = 2, blank= True, null = True)

    def save(self, *args, **kwargs):
        self.amount = self.product.unit_price * self.quantity
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.product_name} - {self.amount}"

class Task(models.Model):
    STATUS_COMPLETION = (
        ('Completed', 'Completed'),
        ('Pending', 'Pending'),
        ('Incomplete', 'Incomplete')
    )
    
    lead = models.ForeignKey("Lead", on_delete = models.CASCADE, related_name = 'created_task')
    notes = models.TextField()
    due_date = models.DateField(null = True, blank= True)
    assigned_to = models.ForeignKey("Agent", on_delete = models.CASCADE, related_name = 'assigned_task', blank = True, null = True)
    status = models.CharField(choices = STATUS_COMPLETION, max_length= 20)

    def __str__(self):
        return self.description
    
def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user = instance)

post_save.connect(post_user_created_signal, sender=User)
