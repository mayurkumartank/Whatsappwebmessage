from rest_framework.views import APIView
from rest_framework import viewsets,status
from rest_framework.response import Response
from ChatBot.serializer import *
from ChatBot.models import *
from user_agents import parse
from selenium import webdriver
from datetime import datetime



class CheckUserApi(APIView):
    def post(self,request):
        serializer = CheckUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']     
            return Response({'status':"True",'message': 'valid User',"email":user[0].email,"end_date":user[0].message_end_date}, status=status.HTTP_200_OK)
        return Response({'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class CreateMessageApi(APIView):
    def post(self,request):
        serializer = CreateMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Create Message successful!'}, status=200)
        return Response({'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class GetMessageApi(APIView):
    def get(self,request):
        user_name = request.data.get("user_name")
        if user_name:  
            try:
                get_user = CustomUser.objects.get(email=user_name)
                if get_user:
                    get_user_message = MessageModel.objects.filter(user_name=get_user.id)
                    serializer = CreateMessageSerializer(get_user_message,many=True)
                    return Response({'data': serializer.data}, status=status.HTTP_200_OK)
            except:
                return Response({'error':'User is not found.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'User Name are reqired.'}, status=status.HTTP_400_BAD_REQUEST)


import os
import time
import qrcode
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import glob
# class GenrateQrcode(APIView):
#     def post(self,request):
def get_latest_file(folder_path):
    # Get a list of all files in the folder
    all_files = glob.glob(os.path.join(folder_path, '*'))

    # If the folder is empty, return None
    if not all_files:
        return None

    # Get the latest file based on the creation time
    latest_file = max(all_files, key=os.path.getctime)
    
    return latest_file


class GenrateQrcode(APIView):
    def post(self,request):
        user_name  = request.data.get("user_name")
        if user_name:
            try:
                get_user = CustomUser.objects.get(email=user_name)
                # full_path = os.path.join(os.getcwd(),user_name)
                custom_user_data_dir = os.path.join(os.getcwd(), "chrome-data",user_name)
                chromedriver_path  = "chromedriver.exe"
                if not os.path.exists(custom_user_data_dir):
                    os.makedirs(custom_user_data_dir)
                print(custom_user_data_dir)
                send_options = webdriver.ChromeOptions()
                send_options.add_argument("--disable-gpu")
                send_options.add_argument(f"webdriver.chrome.driver={chromedriver_path}")
                send_options.add_argument(f"--user-data-dir={custom_user_data_dir}")
                send_options.add_argument("--log-level=3")  # Mute console logs
                send_options.add_argument("user-agent=User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
                send_options.add_argument("--headless")
                driver = webdriver.Chrome(options=send_options)
                driver.get("https://web.whatsapp.com/")
                time.sleep(5)
                data_ref = None
                while data_ref is  None:
                    try:
                        message = driver.find_element(By.XPATH, '//div/div[@class="_19vUU"]')
                        data_ref = message.get_attribute("data-ref")
                        print(data_ref)
                        if data_ref:
                            break
                    except:
                        pass
                    time.sleep(2)
                        
                response_data = {'message': 'aaaaaa'}
                if data_ref is not None:
                    try:
                        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
                        qr.add_data(data_ref)
                        qr.make(fit=True)

                        qr_image = qr.make_image(fill_color="black", back_color="white")
                        full_path = os.path.join("media","qr_code",user_name)
                        if not os.path.exists(full_path):
                            os.makedirs(full_path)
                        current_datetime_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                        filename = f"{user_name}_qr_{current_datetime_str}.png"
                        qr_image.save(os.path.join(full_path, filename))
                        response_data = {'message': f'{data_ref}'}
                        return Response(response_data, status=200)
                    except Exception as e:
                        print(e,"error os ?????????????")
            except Exception as e:
                print(e,"error is <>")
                return Response({'error':'User is not found.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'User Name are reqired.'}, status=status.HTTP_400_BAD_REQUEST)
