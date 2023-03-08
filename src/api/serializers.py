from rest_framework import serializers
from classifr.models import Historique

class HistoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Historique
        fields='__all__'
        
        
