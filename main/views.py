from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import auth, User
from django.contrib import auth
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime, date
from main import views
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
import shutil
import os
import io
import requests
import json
from urllib.parse import quote
from django.http import FileResponse
from django.utils.crypto import get_random_string
from pimux import function

@login_required(login_url='login')
def home(request):
	x=function.misc()
	if request.method=="POST" and request.POST.get('setBright')=="True":
		bright=int(request.POST.get('bright',''))
		if bright >= 0 and bright <=255:
			x.brightness(bright)
			messages.add_message(request,messages.SUCCESS,"Brightness changed successfuly!")
		else:
			messages.add_message(request,messages.WARNING,"Please enter a value betweeen 0 and 255")
	if request.method=="POST" and request.POST.get('vibrate')=="True":
		vib=int(request.POST.get('duration',''))
		x.vibrate(vib)
		messages.add_message(request,messages.SUCCESS,"Phone Vibrated!")
	if request.method=="POST" and request.POST.get('telephone')=="True":
		phone=request.POST.get('number','')
		if len(phone) == 10:
			x.telephonycall(phone)
			messages.add_message(request,messages.SUCCESS,"Calling from phone")
		else:
			messages.add_message(request,messages.WARNING,"Please enter a valid phone number")
	torch=x.torch()
	battery=x.battery()
	return render(request,"home.html",{"battery":battery,"torch":torch})
@login_required(login_url='login')
def torch(request,value):
	x=function.misc()
	if value == "True":
		x.torch(True)
		messages.add_message(request,messages.SUCCESS,"Torch switched on!")
	else:
		messages.add_message(request,messages.SUCCESS,"Torch switched off!")
		x.torch(False)
	return redirect('home')
@login_required(login_url='login')
def click_photo(request, cam_type):
	cam_type=0 if cam_type=="rear" else 1 
	x=function.camera()
	img_name=get_random_string(length=16)+".jpg"
	x.takephoto(cid=cam_type,saveas="~/termux_django/media/images/"+img_name)
	click=clicked_photo(photo_name="/images/"+img_name)
	click.save()
	messages.add_message(request,messages.SUCCESS,"Image Clicked Successfuly!")
	return redirect(home)
@login_required(login_url='login')
def photos(request):
	data=clicked_photo.objects.all()
	return render(request,"photos.html",{"data":data})

def login(request):
	if request.method=="POST":
		username = request.POST.get('username','')
		password = request.POST.get('password','')
		user = auth.authenticate(username=username, password=password)
		if user:
			auth.login(request,user)
			return redirect("home")
		else:
			messages.add_message(request,messages.WARNING,"Invalid Username or Password")
			return render(request,"login.html")
	else:
		return render(request,"login.html")

@login_required(login_url='login')
def logout(request):
	auth.logout(request)
	return redirect('login')