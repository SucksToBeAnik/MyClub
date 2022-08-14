from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event,Venue
# import user model
from django.contrib.auth.models import User
from .forms import VenueForm, EventForm,EventFormAdmin
from django.http import HttpResponse
import csv

# imports for pdf file download
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# import pagination stuff
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q


def admin_approval(request):
    event_count=Event.objects.all().count()
    venue_count=Venue.objects.all().count()
    user_count=User.objects.all().count()
    pending=Event.objects.filter(approved=False).count()

    event_list=Event.objects.order_by('-event_date')
    if request.user.is_superuser:
        if request.method=='POST':
            messages.success(request,'Evnents approvals have been updated!')
            id_list=request.POST.getlist('boxes')
            event_list.update(approved=False)
            for i in id_list:
                Event.objects.filter(pk=int(i)).update(approved=True)
            return redirect('list-events')
        else:
            context={
            'event_list':event_list,
            'event_count':event_count,
            'venue_count':venue_count,
            'user_count':user_count,
            'pending':pending
        }
            return render(request, 'events/admin_approval.html',context) 
    else:
        messages.success(request, 'You are not authorized to view this page!')
        return redirect('home')

    

# create my events page
def my_events(request):
    
    if request.user.is_authenticated:
        me=request.user.id
        events=Event.objects.filter(attendees=me)

        context={
            'events':events,
        }
        return render(request, 'events/my_events.html',context)
    else:
        messages.success(request, 'You are not authorized to view this page. please login to access.')
        return redirect('login')
    

# download pdf file
def venue_pdf(request):
    # create Bytestream buffer
    buf = io.BytesIO()
    # create a canvas
    c=canvas.Canvas(buf,pagesize=letter,bottomup=0)
    # create a text obj
    textobj=c.beginText()
    textobj.setTextOrigin(inch,inch)
    textobj.setFont('Helvetica', 14)

    # add some lines of text
    lines=[]
    venues=Venue.objects.all()
    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append(" ")
    
    for line in lines:
        textobj.textLine(line)
    
    c.drawText(textobj)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf,as_attachment=True,filename='venue.pdf')
    return response


# download csv file
def venue_csv(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Description']='attachment, filename=venues.csv'
    writer=csv.writer(response)
    venues=Venue.objects.all()
    # add header to the csv file
    writer.writerow(['Venue Name','Address','Zip Code','Phone','Web','Email'])
    for venue in venues:
      writer.writerow([venue.name,venue.address,venue.zip_code,venue.phone,venue.web,venue.email_address])
    
    return response

def venue_text(request):
    response=HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'
    venues=Venue.objects.all()
    lines=[]
    for venue in venues:
        lines.append(f"{venue}\n")

    # lines=["Hi! I am Anik\n",
    # "I am cse major undergrad student"]
    # write this lines to a text file
    response.writelines(lines)
    return response

# delete a venue
def delete_venue(request,venue_id):
    venue=Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list-venues')

# delete an event
def delete_event(request,event_id):
    event=Event.objects.get(pk=event_id)
    if request.user==event.manager or request.user.is_superuser :
        event.delete()
        messages.success(request,"Event successfully deleted!")
    else:
        messages.success(request,'You are not authorized to delete this event!')

    
    return redirect('list-events')


def update_event(request,event_id):
    event=Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form=EventFormAdmin(request.POST or None,instance=event)
    else:
        form=EventForm(request.POST or None,instance=event)

    
    if form.is_valid():
        form.save()
        return redirect('list-events')
    context={
        'event':event,
        'form':form,
    }
    return render(request,'events/update_event.html',context)


def add_event(request):
    submitted=False
    if request.method == 'POST':
        if request.user.is_superuser:
            form=EventFormAdmin(request.POST)
            if form.is_valid():
                event=form.save(commit=False)
                event.approved=True
                event.save()
                return HttpResponseRedirect('/add_event?submitted=True')
        else:
            form=EventForm(request.POST)
            if form.is_valid():
                event=form.save(commit=False)
                event.manager=request.user
                event.save()
                messages.success(request, 'Your event has been posted. Wait for an Admin approval.')
                return HttpResponseRedirect('/add_event?submitted=True')
            


    else:
        if request.user.is_superuser:
            form=EventFormAdmin
        else:
            form=EventForm

        if 'submitted' in request.GET:
            submitted=True
    
    context={
        'form':form,
        'submitted':submitted,
    }
    return render(request,'events/add_event.html',context)

def update_venue(request,venue_id):
    venue=Venue.objects.get(pk=venue_id)
    # form=VenueForm(request.POST or None,instance=venue)
    # if form.is_valid():
    #     form.save()
    #     return redirect('list-venues')
    if request.method=='POST':
        form=VenueForm(request.POST,request.FILES,instance=venue)
        if form.is_valid():
            form.save()
            return redirect('list-venues')
    else:
        form=VenueForm(instance=venue)

    context={
        'venue':venue,
        'form':form,
    }
    return render(request,'events/update_venue.html',context)

def search_venues(request):
    if request.method=='POST':
        searched=request.POST.get('searched')
        venues=Venue.objects.filter(name__icontains=searched)
        context={
            'searched':searched,
            'venues':venues,
            }
        return render(request,'events/search_venues.html',context)
    else:
        context={}
        return render(request,'events/search_venues.html',context)

# search events
def search_events(request):
    if request.method=='POST':
        searched=request.POST.get('searched')
        events=Event.objects.filter(Q(name__icontains=searched) | Q(manager__username__icontains=searched))
        context={
            'searched':searched,
            'events':events,
            }
        return render(request,'events/search_events.html',context)
    else:
        context={}
        return render(request,'events/search_events.html',context)

    

def show_venue(request,venue_id):
    venue=Venue.objects.get(pk=venue_id)
    venue_owner=User.objects.get(pk=venue.owner)
    context={
        'venue':venue,
        'venue_owner':venue_owner,
    }
    return render(request,'events/show_venue.html',context)

def list_venues(request):
    venue_list=Venue.objects.all()

    # set up pagination

    p=Paginator(Venue.objects.all().order_by('name'), 2)
    page=request.GET.get('page')
    venues=p.get_page(page)
    nums=venues.paginator.num_pages*'a'
    context={
        'venue_list':venue_list,
        'venues':venues,
        'nums':nums
    }
    return render(request,'events/venue.html',context)

def add_venue(request):
    submitted=False
    if request.method == 'POST':
        form=VenueForm(request.POST,request.FILES)
        if form.is_valid():
            venue=form.save(commit=False)
            venue.owner=request.user.id
            venue.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form=VenueForm
        if 'submitted' in request.GET:
            submitted=True
    
    context={
        'form':form,
        'submitted':submitted,
    }
    return render(request,'events/add_venue.html',context)


def home(request,year=datetime.now().year,month=datetime.now().strftime('%B')):

    month=month.capitalize()
    # convert month from name to number
    month_number=list(calendar.month_name).index(month)
    month_number=int(month_number)

    # create a calendar
    cal=HTMLCalendar().formatmonth(year,month_number)

    # current year
    now=datetime.now()
    current_year=now.year

    # query current motnh events
    event_list=Event.objects.filter(event_date__year=year,event_date__month=month_number)
    # current time
    time=now.strftime('%I:%M:%S %p')
    context={
        'year':year,
        'month':month,
        'cal':cal,
        'current_year':current_year,
        'time':time,
        'event_list':event_list,
    }
    return render(request,'events/home.html',context)

def all_events(request):
    event_list=Event.objects.all().order_by('event_date')
    for i in event_list:
        print(i.attendees.all())

    context={
        'event_list':event_list
    }
    return render(request,'events/event_list.html',context)
