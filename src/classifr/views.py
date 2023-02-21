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
import keras.backend as K
from keras.models import load_model
from keras.utils import load_img, img_to_array


# Create your views here.

def index(request):
    return redirect('upload')

def upload(request):
    return render(request,'upload.html')

def resultat(request):
    food_list = ['apple_pie', 'beef_carpaccio', 'bibimbap', 'cup_cakes', 'foie_gras', 'french_fries', 
                 'garlic_bread', 'pizza', 'spring_rolls', 'spaghetti_carbonara', 'strawberry_shortcake']
    
    # K.clear_session()
    model11 = load_model('classifr/static/model/model11.hdf5',compile = False)
    
    image='applepie.jpg'
    
    path="/images/"+image
    context={}
    def predict_class(model, image):
        image = load_img(path='classifr/static/images/'+image, target_size=(299, 299))
        image = img_to_array(image)                    
        image = np.expand_dims(image, axis=0)         
        image /= 255.                                      
        pred = model.predict(image)
        index = np.argmax(pred)
        food_list.sort()
        label = food_list[index]
        perc=round(np.amax(pred)*100,2)
        result=label +'  '+str(perc)+' %'
        print(label +'  '+str(perc)+' %' )
        return result
        # print(np.amax(pred))
    context={'path':path,'result':predict_class(model11, image)}    
           
             
    return render(request,'resultat.html',context)

@login_required(login_url='/classifr/login')
def historique(request):
    return render(request,'historique.html')