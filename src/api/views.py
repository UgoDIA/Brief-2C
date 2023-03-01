from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from  classifr.models import Classe,Model,Historique
from .serializers import HistoSerializer
# Create your views here.

@api_view(['GET'])
def getHisto(request):
    null=request.query_params.get('null',None)
    histo=Historique.objects.all()
    if null =="false":
        histo=Historique.objects.exclude(classe_correcte=None)
    serializer=HistoSerializer(histo, many=True)
    return Response(serializer.data)
    
@api_view(['GET'])
def getHistoDet(request,pk):
    histo=Historique.objects.get(id_histo=pk)
    serializer=HistoSerializer(histo, many=False)
    return Response(serializer.data)
    
@api_view(['POST'])
def createHisto(request):
    serializer=HistoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def updateHisto(request,pk): 
    histo=Historique.objects.get(id_histo=pk)
    serializer=HistoSerializer(instance=histo,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteHisto(request,pk): 
    histo=Historique.objects.get(id_histo=pk)
    histo.delete()
    return Response("Ligne supprimée")