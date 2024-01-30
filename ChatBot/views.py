import os
import cv2
import time
import qrcode
import re,sys
import tempfile
import pyperclip
import threading
import numpy as np
from ChatBot.models import *
from user_agents import parse
from selenium import webdriver
from django.contrib import messages
from django.http import JsonResponse
from asgiref.sync import sync_to_async
from selenium.webdriver.common.by import By
from django.shortcuts import render,redirect
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from django.contrib.auth import authenticate, login, logout 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from ChatBot.constants import DEFAULT_WAIT,MAIN_SEARCH_BAR__SEARCH_ICON,EXTRACT_SESSION,INJECT_SESSION,QR_CODE,SETUP_INDEXEDDB
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def HomePage(request):
    return render(request,"testing.html")

def SignUpPage(request):
    if request.method == "POST":
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        profile_image = request.FILES.get('Profile_Image')
        password = request.POST['password']
        conform_password = request.POST['confirmpassword']
        if email:
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                messages.error(request,"Invalid email address")
        if password != conform_password:
            messages.error(request,"Password and Conform Password is does not match")
        else:
            check_user = CustomUser.objects.filter(email=email).exists()
            if check_user:
                messages.error(request,"User email alredy exits")
            else:
                if first_name  and last_name and email and password:
                    CustomUser.objects.create_user(email=email,first_name=first_name,user_image=profile_image,last_name=last_name,password=password)
                    messages.success(request,"Create User Successfully")
                    return redirect("/login/")
                else:
                    messages.error(request,"All data are required.")
    return render(request,"signup.html")

def LoginPage(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        if email and password:
            user = authenticate(email=email, password=password)
            if user is not None:
                if not user.is_active:
                    messages.error(request,'User account is inactive.')
                login(request, user)    
                messages.success(request,"Login Successfully.")
                return redirect("/")
            if not user:
                messages.error(request,"Invalid email or password.")
        else:
            messages.error(request,"Both email and password are required.")
    return render(request,"login.html")

def LogOutPage(request):
    logout(request)
    messages.success(request,"Successfully Logout")
    return redirect("/")

def CheckQrCode(request):
    return render(request,"qr_code.html")





# def handle_uploaded_file(uploaded_file):
#     destination = "./media/uploads/wa/"
#     # Concatenate the destination directory and the file name
#     if not os.path.exists(destination):
#         os.makedirs(destination)

#     file_path = destination + uploaded_file.name

#     with open(file_path, 'wb') as destination_file:
#         for chunk in uploaded_file.chunks():
#             destination_file.write(chunk)

#     return file_path

