from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.db import connection
from os.path import isfile, join
from django.urls import reverse
import os, shutil, psycopg2
import pandas as pd
import numpy as np
from os import walk,listdir
from os.path import isfile, join


# Create your views here.

def index(request):
    return redirect('upload')

def upload(request):
    return render(request,'upload.html')

@login_required(login_url='/classifr/login')
def historique(request):
    return render(request,'historique.html')