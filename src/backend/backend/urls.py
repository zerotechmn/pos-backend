"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from backend.views import *
from backend.middleware.guur import *
from backend.middleware.vatps import *
from oauth2_provider import views

urlpatterns = [
    # Oauth
    path('oauth2/authorize/', views.AuthorizationView.as_view(), name="authorize"),
    path('oauth2/token/', views.TokenView.as_view(), name="token"),

    path('ping/', ping),
    path('admin/', admin.site.urls),
    path('guur/auth/token/', guurAuthToken),
    path('guur/get_product_line/', guurGetProductLine),
    path('guur/get_warehouse/', guurGetWareHouse),
    path('guur/get_pump/', guurGetPump),
    path('guur/get_product/', guurGetProduct),

    path("ebarimt/merchant_tin/", ebarimtMerchantTin),
    path("ebarimt/get_receipt/", eBarimtReceiptransaction),
    path('update_info.json', update_info),
]
