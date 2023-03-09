from rest_framework.response import Response
from rest_framework.decorators import api_view
from  classifr.models import Classe,Model,Historique
from .serializers import HistoSerializer
from django.db import connection

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
    result = [getModelStats('model3'),getModelStats('model11')]
    return Response(result)

def getModelStats(model):
    cursor=connection.cursor()
    cursor.execute('''select nom_model,count(*)
                    from historique 
                    where nom_model=%(model)s
                    group by (nom_model)
                    order by nom_model desc''',{"model":model})
    totalModel=cursor.fetchall()
    if not totalModel:
        totalModel=[('0',0)]
    
    cursor.execute('''select nom_model,count(*)
                    from historique 
                    where classe_correcte is null and nom_model=%(model)s
                    group by (nom_model)
                    order by nom_model desc''',{"model":model})
    totalModelSuccess=cursor.fetchall()
    if not totalModelSuccess:
        totalModelSuccess=[('0',0)]
  
    cursor.execute('''select nom_model,count(*)
                    from historique 
                    where classe_correcte is not null and nom_model=%(model)s
                    group by (nom_model)
                    order by nom_model desc''',{"model":model})
    totalModelError=cursor.fetchall()
    if not totalModelError:
        totalModelError=[('0',0)]
 
    cursor.execute('''select classe_predit,count(*)
                    from historique 
                    where nom_model=%(model)s and classe_correcte is null
                    group by (classe_predit)
                    order by 2 desc''',{"model":model})
    topModel=cursor.fetchall()
    if not topModel:
        topModel=[('0',0)]
    
    cursor.execute('''select classe_correcte,count(*)
                    from historique 
                    where nom_model=%(model)s and classe_correcte is not null
                    group by (classe_correcte)
                    order by 2 desc''',{"model":model})
    flopModel=cursor.fetchall()
    if not flopModel:
        flopModel=[('0',0)]

    result={
            "nomModel":model,
            "total":totalModel[0][1],
            "success":totalModelSuccess[0][1],
            "errors":totalModelError[0][1],
            "pourcentage":round(totalModelSuccess[0][1] / totalModel[0][1] * 100,2),
            'top':topModel[0][0],
            'flop':flopModel[0][0],     
        }
    return result


@api_view(['GET'])
def getstatsgraph(request):
    cursor=connection.cursor()
    model=request.query_params.get('model',None)
    ordre=request.query_params.get('ordre',None)
    cursor.execute('''SELECT classe, SUM(bonne_classe) AS bonne_classe, SUM(bonne_classe + mauvaise_classe) AS total
                        FROM (
                        SELECT classe_predit AS classe, COUNT(*) AS bonne_classe, 0 AS mauvaise_classe
                        FROM historique
                        WHERE nom_model = %(model)s AND classe_correcte IS NULL
                        GROUP BY classe_predit
                        UNION ALL
                        SELECT classe_correcte AS classe, 0 AS bonne_classe, COUNT(*) AS mauvaise_classe
                        FROM historique
                        WHERE nom_model = %(model)s AND classe_correcte IS NOT NULL
                        GROUP BY classe_correcte
                        ) AS counts
                        GROUP BY classe
                        ORDER BY total DESC''',{"model":model})
    topModel=cursor.fetchall()
    
    result = []

    for item in topModel:
        className = item[0]
        bonne_classe = item[1]
        total = item[2]
        perc = round((bonne_classe/total) * 100, 2)
        result.append((className, perc))
        
    result = [item for item in result if item[0] != "autre"]
    if ordre=="asc":
        result.sort(key=lambda x: x[1])
        return Response(result)
    else:
        result.sort(key=lambda x: x[1], reverse=True)
        return Response(result)
    

@api_view(['GET'])
def hover(request):
    cursor=connection.cursor()
    model=request.query_params.get('model',None)
    label=request.query_params.get('label',None)
    cursor.execute('''SELECT classe, SUM(bonne_classe) AS bonne_classe,SUM(mauvaise_classe) AS mauvaise_classe, SUM(bonne_classe + mauvaise_classe) AS total
                        FROM (
                        SELECT classe_predit AS classe, COUNT(*) AS bonne_classe, 0 AS mauvaise_classe
                        FROM historique
                        WHERE nom_model = %(model)s AND classe_correcte IS NULL and classe_predit=%(label)s
                        GROUP BY classe_predit
                        UNION ALL
                        SELECT classe_correcte AS classe, 0 AS bonne_classe, COUNT(*) AS mauvaise_classe
                        FROM historique
                        WHERE nom_model = %(model)s AND classe_correcte =%(label)s
                        GROUP BY classe_correcte
                        ) AS counts
                        GROUP BY classe
                        ORDER BY total DESC''',{"model":model,"label":label})
    result=cursor.fetchall()
    if not result:
        result=[('0',0)]
    return Response(result)
    
