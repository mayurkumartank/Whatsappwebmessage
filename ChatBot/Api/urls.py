from .api import *
from django.urls import path

urlpatterns = [
    path("checkuser/",CheckUserApi.as_view(),name="checkuser"),
    path("createmessage/",CreateMessageApi.as_view(),name="createmessage"),
    path("getmessage/",GetMessageApi.as_view(),name="getmessage"),
    path("qrcode/",GenrateQrcode.as_view(),name="qrcode")
]