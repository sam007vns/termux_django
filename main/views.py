from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import auth, User
from django.contrib import auth
from django.contrib.auth import authenticate, logout, login
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

def home(request):
	return render(request,"home.html")

def click_photo(request):
	x=function.camera()
	img_name=get_random_string(length=16)+".jpg"
	x.takephoto(cid=0,saveas="~/termux_django/media/images/"+img_name)
	click=clicked_photo(photo_name=img_name)
	click.save()
	messages.add_message(request,messages.SUCCESS,"Image Clicked Successfuly!")
	return redirect(home)
def photos(request):
	return render(request,"photos.html")
