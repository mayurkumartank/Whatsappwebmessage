from django.urls import path
from ChatBot import views

urlpatterns = [
    path('', views.HomePage),
    path('login/', views.LoginPage),
    path('signup/', views.SignUpPage),
    path("logout/",views.LogOutPage),
    path("qrcode/",views.CheckQrCode),
    # path("sendmessage/",views.SendMessage),
    # path("test/",views.HomePage2),
    # path("api/checkuser/",views.CheckUserApi.as_view(),name="checkuser")
]