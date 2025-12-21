from rest_framework import serializers
from .models import t_cargo, t_area, t_lista

class cargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = t_cargo
        fields = ['id','codigo','nombre','estado']
        
class areaSerializer(serializers.ModelSerializer):
    class Meta:
        model = t_area
        fields = ['id','codigo','nombre','estado']
        

class listaSerializer(serializers.ModelSerializer):
    class Meta:
        model = t_lista
        fields = ['id','codigo','nombre','descripcion']
        
