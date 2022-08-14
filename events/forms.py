from django import forms
from django.forms import ModelForm
from .models import Venue,Event

# create a venue form

class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = ('name','address','zip_code','phone','web','email_address','image')
        labels={
            'name':'',
            'address':'',
            'zip_code':'',
            'phone':'',
            'web':'',
            'email_address':'',
            'image':'',
        }
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter venue name'}),
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':'Address',}),
            'zip_code':forms.TextInput(attrs={'class':'form-control','placeholder':'Zip Code',}),
            'phone':forms.TextInput(attrs={'class':'form-control','placeholder':'Phone Number',}),
            'web':forms.TextInput(attrs={'class':'form-control','placeholder':'Web Address',}),
            'email_address':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email',}),
        }

# admin/superuser event form
class EventFormAdmin(ModelForm):
    class Meta:
        model = Event
        fields = ('name','event_date','venue','manager','attendees','description')
        labels={
            'name':'',
            'event_date':'YYYY-MM-DD HH:MM:SS',
            'venue':'Venue',
            'manager':'Manager',
            'attendees':'',
            'description':'',
            
        }
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter event name'}),
            'event_date':forms.TextInput(attrs={'class':'form-control','placeholder':'Event date',}),
            'venue':forms.Select(attrs={'class':'form-select','placeholder':'venue',}),
            'manager':forms.Select(attrs={'class':'form-select','placeholder':'Manager',}),
            'attendees':forms.SelectMultiple(attrs={'class':'form-control','placeholder':'Attendees',}),
       
            'description':forms.Textarea(attrs={'class':'form-control','placeholder':'Add a description',}),
            }

# user event form
class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('name','event_date','venue','attendees','description')
        labels={
            'name':'',
            'event_date':'YYYY-MM-DD HH:MM:SS',
            'venue':'Venue',
            'attendees':'',
            'description':'',
            
        }
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter event name'}),
            'event_date':forms.TextInput(attrs={'class':'form-control','placeholder':'Event date',}),
            'venue':forms.Select(attrs={'class':'form-select','placeholder':'venue',}),
            'attendees':forms.SelectMultiple(attrs={'class':'form-control','placeholder':'Attendees',}),
            'description':forms.Textarea(attrs={'class':'form-control','placeholder':'Add a description',}),
            }