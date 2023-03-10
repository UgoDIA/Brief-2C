"""classifr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from . import views
from .views import index
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index, name="index"),
    path('classifr/', views.upload, name="upload"),
    path('classifr/',include('identification.urls')),
    path('classifr/historique/',views.historique, name='historique'),
    path('classifr/resultat/', views.resultat, name='resultat'),
    path('classifr/retour/', views.btreturn, name='btreturn'),
    path('classifr/',include('api.urls')),
    path('classifr/multiple/', views.uploadmultiple, name="uploadmultiple"),
    path('classifr/resultatmultiple/', views.resultatmultiple, name="resultatmultiple"),
]

if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  