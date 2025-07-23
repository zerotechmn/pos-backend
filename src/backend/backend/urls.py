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
from backend.terminal.terminal import *
from oauth2_provider import views

urlpatterns = [
    # Oauth
    path('oauth2/authorize/', views.AuthorizationView.as_view(), name="authorize"),
    path('oauth2/token/', views.TokenView.as_view(), name="token"),

    path('ping/', ping),
    path('admin/', admin.site.urls),
    path('terminal/set_terminal/', SetTerminalView.as_view(), ),

    path('guur/auth/token/', GuurAuthTokenView.as_view()),
    path('guur/get_product_line/', GuurGetProductLineView.as_view()),
    path('guur/get_warehouse/', GuurGetWareHouseView.as_view()),
    path('guur/get_pump/', GuurGetPumpView.as_view()),
    path('guur/get_product/', GuurGetProductView.as_view()),

    path("ebarimt/merchant_tin/", EbarimtMerchantTinView.as_view()),
    path("ebarimt/get_receipt/", EBarimtReceiptransactionView.as_view()),
    path('update_info.json', update_info),
]
