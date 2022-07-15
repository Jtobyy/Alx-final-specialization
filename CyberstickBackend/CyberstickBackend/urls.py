"""CyberstickBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from core.views import *
from core.admin import cyberstick_site
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    #path('admin/', admin.site.urls),
    path('cyberstickadmin/custom_dashboard/', CustomDashboardView.as_view(), name='custom_dashboard'),
    path('cyberstickadmin/custom_settings/', CustomSettingsView.as_view(), name='custom_settings'),
    path('cyberstickadmin/login/', CyberstickLoginView.as_view(), name='login'),
    path('cyberstickadmin/', cyberstick_site.urls, name='admin'),
    path('cyberstick/products/', ProductView.as_view(), name="products"),
    path('cyberstick/customers/', CustormerView.as_view(), name="customers"),
    path('cyberstick/orders/', OrderListView.as_view(), name="orders"),
    path('cyberstick/orders/<int:pk>', SingleOrderView.as_view(), name="order"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
