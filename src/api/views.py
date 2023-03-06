from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from  classifr.models import Classe,Model,Historique
from .serializers import HistoSerializer
from django.db import connection
from django.db.models import Count
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


@api_view(['GET'])
def getstats(request):
    cursor=connection.cursor()
    cursor.execute('''select nom_model,count(*)
                    from historique 
                    group by (nom_model)
                    order by nom_model desc''')
    totalModel=cursor.fetchall()
    # print(totalModel)
    cursor.execute('''select nom_model,count(*)
                    from historique 
                    where classe_correcte is null 
                    group by (nom_model)
                    order by nom_model desc''')
    totalModelSuccess=cursor.fetchall()
    # print(totalModelSuccess)
    cursor.execute('''select nom_model,count(*)
                    from historique 
                    where classe_correcte is not null 
                    group by (nom_model)
                    order by nom_model desc''')
    totalModelError=cursor.fetchall()
    # print(totalModelError)
    cursor.execute('''select classe_predit,count(*)
                    from historique 
                    where nom_model='model3' and classe_correcte is null
                    group by (classe_predit)
                    order by 2 desc''')
    topModel3=cursor.fetchall()
    # print(topModel3)
    cursor.execute('''select classe_correcte,count(*)
                    from historique 
                    where nom_model='model3' and classe_correcte is not null
                    group by (classe_correcte)
                    order by 2 desc''')
    flopModel3=cursor.fetchall()
    # print(flopModel3)
    cursor.execute('''select classe_predit,count(*)
                    from historique 
                    where nom_model='model11' and classe_correcte is null
                    group by (classe_predit)
                    order by 2 desc''')
    topModel11=cursor.fetchall()
    # print(topModel11)
    cursor.execute('''select classe_correcte,count(*)
                    from historique 
                    where nom_model='model11' and classe_correcte is not null
                    group by (classe_correcte)
                    order by 2 desc''')
    flopModel11=cursor.fetchall()
    # print(flopModel11)
    result=[{
            "nomModel":totalModel[0][0],
            "total":totalModel[0][1],
            "success":totalModelSuccess[0][1],
            "errors":totalModelError[0][1],
            "pourcentage":round(totalModelSuccess[0][1] / totalModel[0][1] * 100,2),
            'top':topModel3[0][0],
            'flop':flopModel3[0][0],     
        },
          {
            "nomModel":totalModel[1][0],
            "total":totalModel[1][1],
            "success":totalModelSuccess[1][1],
            "errors":totalModelError[1][1],
            "pourcentage":round(totalModelSuccess[1][1] / totalModel[1][1] * 100,2),
            'top':topModel11[0][0],
            'flop':flopModel11[0][0],            
    }]
    print(result)
    return Response(result)

@api_view(['GET'])
def getstatsgraph(request):
    cursor=connection.cursor()
    model=request.query_params.get('model',None)
    top=request.query_params.get('top',None)
    if model=="model3":
        if top=="true":
            cursor.execute('''select classe_predit,count(*)
                            from historique 
                            where nom_model='model3' and classe_correcte is null
                            group by (classe_predit)
                            order by 2 desc''')
            topModel3=cursor.fetchall()
            print(type(topModel3))
            return Response(topModel3)
        elif top=="false":
            cursor.execute('''select classe_correcte,count(*)
                            from historique 
                            where nom_model='model3' and classe_correcte is not null
                            group by (classe_correcte)
                            order by 2 desc''')
            flopModel3=cursor.fetchall()
            return Response(flopModel3)
    elif model=="model11":
        if top=="true":
            cursor.execute('''select classe_predit,count(*)
                            from historique 
                            where nom_model='model11' and classe_correcte is null
                            group by (classe_predit)
                            order by 2 desc''')
            topModel11=cursor.fetchall()
            return Response(topModel11)
        elif top=="false":
            cursor.execute('''select classe_correcte,count(*)
                            from historique 
                            where nom_model='model11' and classe_correcte is not null
                            group by (classe_correcte)
                            order by 2 desc''')
            flopModel11=cursor.fetchall()
            return Response(flopModel11)
    return Response({})