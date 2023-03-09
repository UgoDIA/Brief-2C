from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/histo/', views.getHisto, name="histo"),
    path('api/histo/<str:pk>/', views.getHistoDet, name="histoDet"),
    path('api/createhisto/', views.createHisto, name="histoCreate"),
    path('api/updatehisto/<str:pk>/', views.updateHisto, name="histoUpdate"),
    path('api/deletehisto/<str:pk>/', views.deleteHisto, name="histoDelete"),
    path('api/stats/', views.getstats, name="stats"),
    path('api/statsgraph/', views.getstatsgraph, name="statsgraph"),
    path('api/statsgraph/hover/', views.hover, name="hover"),
]