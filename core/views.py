from django.shortcuts import render,redirect
from core.forms  import *
from core.models import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os
from django.conf import settings
from random import randint

def home(request):
    return render(request, "home.html")

def signup_view(request):

    if request.method == 'POST' and request.FILES['file1']:
        proof = request.FILES['file1']
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        org = request.POST.get('reg')
        ticket = request.POST.get('ticket')
        token = randint(101,1000000001)
        Candidate.objects.create(name=name,phone_number=mobile,email=email,proof=proof,org=org,ticket=ticket,token=token)
        s = "Your Event Is Sucessfully added with token number " + str(token)
        return HttpResponse(s)
    return render(request, "signup.html")

def signin_view(request):

    if request.method == 'POST':
        username = request.POST.get('uname')
        pswd = request.POST.get('psw')
        user = authenticate(username=username, password=pswd)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('admin_home'))
            else:
                messages.info(request, 'User is flagged Inactive. Drop mail to admin to reactivate your account')
                return HttpResponseRedirect(reverse('admin_home'))
        else:
            messages.info(request, 'Invalid login details given')
            return HttpResponseRedirect(reverse('login'))
    return render(request,"login.html")

def contact_view(request):
    return render(request,"team_info.html")    

@login_required(login_url='/login/')
def add_home_view(request):
    self_ct = Candidate.objects.filter(org="SELF").count()
    cor_ct = Candidate.objects.filter(org="CORPORATE").count()
    grp_ct = Candidate.objects.filter(org="GROUP").count()
    oth_ct = Candidate.objects.filter(org="OTHERS").count()
    mydic = {
            "Self":self_ct,
            "Corporate":cor_ct,
            "Group":grp_ct,
            "Others":oth_ct,
        }
    context = {
        'tot': self_ct + oth_ct + grp_ct + cor_ct,
    }
    context["data"] = mydic
    registrations = Candidate.objects.all()
    context["registrations"] = registrations
    return render(request, "events.html", context)


@login_required(login_url='/login/')
def receipt_view(request, pk):
    obj = Candidate.objects.get(id=pk)
    context = {
        'obj' : obj,
    }
    return render(request, "receipt.html", context)

@login_required
def signout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))