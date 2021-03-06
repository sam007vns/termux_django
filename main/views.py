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
from pimux import function, scrip
import ast
import time

@login_required(login_url='login')
def home(request):
	x=function.misc()
	y=function.volume()
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
	if request.method=="POST" and request.POST.get('setVolume')=="True":
		volume=int(request.POST.get('volume',''))
		if volume >= 0 and volume <= 15:
			y.volumeControl(stream='music', volume=volume)
			messages.add_message(request,messages.SUCCESS,"volume chnaged successfuly")
		else:
			messages.add_message(request,messages.WARNING,"Please enter a number between 0 to 10")
	if request.method=="POST" and request.POST.get('pushNotification') == "True":
		display_msg=request.POST.get('msgText')
		if len(display_msg) > 0:
			display_msg='"'+display_msg+'"'
			scrip.compute(['termux-notification --content '+str(display_msg)])
			messages.add_message(request,messages.SUCCESS,"Notification displayed on phone!")
			return redirect('home')
		messages.add_message(request,messages.WARNING,"Please enter a valid message to display on notifiction!")
	if request.method=="POST" and request.POST.get('popNotification') == "True":
		display_msg=request.POST.get('msgText')
		background_color=request.POST.get('bcolor','gray')
		text_color=request.POST.get('tcolor','white')
		if len(display_msg) > 0:
			display_msg='"'+display_msg+'"'
			scrip.compute(["termux-toast "+ "-b " + background_color+  " -c "+ text_color+ " " +str(display_msg)])
			messages.add_message(request,messages.SUCCESS,"Tost Notification displayed on phone!")
			return redirect('home')
		messages.add_message(request,messages.WARNING,"Please enter a valid message to display on notifiction!")
		return redirect('home')
	if request.method=="POST" and request.POST.get('sendSMSnow') == "True":
		msg_body=request.POST.get('msgText')
		recipient=request.POST.get('recepientNumbers')
		recepient=recipient.split(',')
		for x in range(0, len(recepient)):
			if recepient[x].isdigit() and len(recepient[x]) ==10:
				scrip.compute(["termux-sms-send -n "+ recepient[x] + " " +str(msg_body)])
		messages.add_message(request,messages.SUCCESS,"Message sent successfuly!")
		return redirect('home')
	if request.method=="POST" and request.POST.get('execCommand') == "True":
		command=request.POST.get('command')
		wtime=request.POST.get('wtime')
		wtime = int(wtime) if wtime.isdigit() else 0
		res=scrip.compute(['"'+command+'"'])
		time.sleep(wtime)
		messages.add_message(request,messages.SUCCESS,"Result: "+ str(res) )
		return redirect('home')
	battery=ast.literal_eval(x.battery())
	return render(request,"home.html",{"battery":battery})
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
@login_required(login_url='login')
def get_location(request):
	loc = scrip.compute(['termux-location'])
	loc = ast.literal_eval(loc['output'])
	save_last=last_location(latitude=loc["latitude"],longitude=loc["longitude"],altitude=loc["altitude"],accuracy=loc["accuracy"],speed=loc["speed"],elapsedMs=loc["elapsedMs"],provider=loc["provider"])
	save_last.save()
	last_locs=last_location.objects.all()
	return render(request,"location.html",{"loc":loc,"last":last_locs})

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
def record_audio_now(request):
	if request.method == "POST":
		duration=request.POST.get('duration')
		if not duration.isdigit() or not int(duration)>=1:
			messages.add_message(request,messages.WARNING,"Duration must be greater than 1 sec.")
			return redirect('home')
		aud_file_name=get_random_string(length=16)+".mp3"
		path_toSave = "~/termux_django/media/musics/"+aud_file_name
		scrip.compute(['termux-microphone-record -d -f '+path_toSave+' -l '+duration])
		time.sleep(int(duration))
		save_aud=record_audio(audio="/musics/"+aud_file_name,time_sec=duration)
		save_aud.save()
		messages.add_message(request,messages.SUCCESS,"Audio recording saved successfuly!")
		return redirect('home')
	return redirect('home')
@login_required(login_url='login')
def view_audio_records(request):
	audio=record_audio.objects.all()
	return render(request,"view_audio_recording.html",{"data":audio})
@login_required(login_url='login')
def view_call_logs(request):
	row='10'
	if request.method=="POST":
		check=request.POST.get('entry')
		row = check if check.isdigit() else '10'
	data=scrip.compute(['termux-call-log -l '+row])
	data=ast.literal_eval(data['output'])
	return render(request,"view_call_logs.html",{"data":data})
@login_required(login_url='login')
def view_sms_logs(request):
	row='10'
	if request.method=="POST":
		check=request.POST.get('entry')
		row = check if check.isdigit() else '10'
	data=scrip.compute(['termux-sms-list -d -n -t all -l '+row])
	data=json.loads(data['output'])
	return render(request,"view_sms_logs.html",{"data":data})
@login_required(login_url='login')
def logout(request):
	auth.logout(request)
	return redirect('login')