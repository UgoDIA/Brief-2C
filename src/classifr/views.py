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
from .models import Classe,Model,Historique
from datetime import date


# Create your views here.

def index(request):
    return redirect('upload')

def upload(request):
    model=Model.objects.values_list('nom_model',flat=True)
    context={"model":model}
    if request.method == 'POST':  
        uploaded_image = request.FILES['image']
        fs=FileSystemStorage()
        fs.save(uploaded_image.name, uploaded_image)
        image=str(uploaded_image)
        modelx=request.POST['model']
        if modelx == "model11" :
            food_list = ['tarte_pomme', 'carpaccio_boeuf', 'bibimbap', 'cupcakes', 'foie_gras', 'frites', 
                    'pain_a_l\'ail', 'pizza',  'spaghetti_carbonara','rouleaux_printemps', 'gateau_framboise']
            model = load_model('classifr/static/model/model11.hdf5',compile = False)
        elif modelx=="model3":
            food_list = ['tarte_pomme', 'omelette', 'pizza']
            model = load_model('classifr/static/model/model3.hdf5',compile = False)
        def predict_class(model, image):
            image = load_img(path='classifr/static/images/'+image, target_size=(299, 299))
            image = img_to_array(image)                    
            image = np.expand_dims(image, axis=0)         
            image /= 255.                                      
            pred = model.predict(image)
            index = np.argmax(pred)
            label = food_list[index]
            perc=round(np.amax(pred)*100,2)
            # print(label +'  '+str(perc)+' %' )
            return label,perc
        result=(predict_class(model,image))
        classe_pred=Classe.objects.get(nom_classe=result[0])
        modelname=Model.objects.get(nom_model=modelx)
        histo=Historique(nom_image=image,precision=result[1],classe_predit=classe_pred,nom_model=modelname,date_pred=date.today())
        histo.save()
        label=result[0]
        food_list.remove(label)
        food_list.append("autre")
        request.session['histo']=histo.id_histo
        request.session['food_list']=food_list
    
        return HttpResponseRedirect('resultat')
    return render(request, 'upload.html',context)

def resultat(request):
    try:
        histo=request.session['histo']
        food_list=request.session['food_list']
        histo=Historique.objects.get(id_histo=histo)
        label=histo.classe_predit.nom_classe
        precision=histo.precision
        path="/images/"+histo.nom_image
        # classe=Classe.objects.values_list('nom_classe',flat=True)
        context={'path':path,'label':label,'precision':precision,'histo':histo,'food_list':food_list} 
        if request.method =='POST':
            try:
                x=request.POST["classec"] 
                classe=Classe.objects.get(nom_classe=x)
                newhisto=Historique(id_histo=histo.id_histo,classe_correcte=classe)
                newhisto.save(update_fields=['classe_correcte'])  
                messages.success(request, ("L'erreur à bien été enregistrée, merci."))
                del request.session['histo']
                return HttpResponseRedirect(reverse('upload'))
            except:    
                messages.error(request, ("Une erreur est survenue lors de l'envoi du formulaire."))
    except:
           return HttpResponseRedirect(reverse('upload'))         
    return render(request,'resultat.html',context)

def btreturn(request):
    try:
        del request.session['histo']
    except:
        pass
    return HttpResponseRedirect(reverse('upload'))
    

@login_required(login_url='/classifr/login')
def historique(request):
    return render(request,'historique.html')