from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Venue(models.Model):
    name = models.CharField('Venue Name',max_length=120)
    address = models.CharField(max_length=300)
    zip_code = models.CharField('Zip code',max_length=15)
    phone = models.CharField('Contact phone',max_length=25,blank=True)
    web = models.URLField('Website address',blank=True)
    email_address = models.EmailField('Email address',blank=True)
    owner=models.IntegerField("Venue Owner ID",blank=False,default=1)
    image=models.ImageField(null=True,blank=True,upload_to='images/')

    def __str__(self):
        return self.name

class MyClubUser(models.Model):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    email=models.EmailField('User email')
 
    def __str__(self):
        return self.first_name + " " + self.last_name

class Event(models.Model):
    name = models.CharField('Event name',max_length=120)
    event_date = models.DateTimeField('Event Date')
    venue=models.ForeignKey(Venue,null=True,blank=True,on_delete=models.CASCADE)
    # venue =models.CharField(max_length=120)
    manager =models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True)
    description = models.TextField(blank=True)
    attendees= models.ManyToManyField(MyClubUser,blank=True)
    approved=models.BooleanField("Approved",default=False)

    def __str__(self):
        return self.name

    @property
    def days_till(self):
        days_left=self.event_date.date()-date.today()
        days_left_stripped=str(days_left).split(",")[0]
        return days_left_stripped
# user event model
