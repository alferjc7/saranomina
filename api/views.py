from argparse import Action
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from api.models import t_cargo, t_area, t_lista
from api.serializer import cargoSerializer, areaSerializer, listaSerializer
from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from rest_framework.decorators import action

class PingApiView(APIView):
    def get(self,request):
        return Response({'mensaje':'Api funcionando correctamente'},
                        status=status.HTTP_200_OK)
    

class SaludoApiView(APIView):
    def get(self,request):
        return Response({'mensaje':'Hola desde DRF'},status=status.HTTP_200_OK)
    def post(self,request):
        nombre = request.data.get("nombre","anonimo")
        return Response({"mensaje":f"hola {nombre}"})
    
class CargoApiView(APIView):
    def get(self,request,pk = None):
        if pk is None:
            cargos = t_cargo.objects.all()
            serializer = cargoSerializer(cargos, many = True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            cargo = get_object_or_404(t_cargo,pk=pk)
            serializer = cargoSerializer(cargo)
            return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request):
        serializer = cargoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete (self,request, pk = None):
        cargo = get_object_or_404(t_cargo,pk=pk)
        cargo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    def put (self, request, pk = None):
        cargo = get_object_or_404(t_cargo,pk=pk)
        carSerializer = cargoSerializer(cargo,request.data)
        if carSerializer.is_valid():
            carSerializer.save()
            return Response(carSerializer.data,status=status.HTTP_200_OK)
        else:
            return Response(carSerializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def patch (self, request, pk = None):
        cargo = get_object_or_404(t_cargo,pk=pk)
        carSerializer = cargoSerializer(cargo,request.data, partial = True)
        if carSerializer.is_valid():
            carSerializer.save()
            return Response(carSerializer.data,status=status.HTTP_200_OK)
        else:
            return Response(carSerializer.errors,status=status.HTTP_400_BAD_REQUEST)

class areaApiView(APIView):
    def get(self,request,pk= None):
        if pk is None:
            area = t_area.objects.all()
            aSerializer = areaSerializer(area, many = True)
            return Response(aSerializer.data,status=status.HTTP_200_OK)
        else:
            area = get_object_or_404(t_area, pk=pk)
            aSerializer = areaSerializer(area)
            return Response(aSerializer.data, status=status.HTTP_200_OK)    
    def post(self,request):
        aSerializer = areaSerializer(data = request.data)
        if aSerializer.is_valid():
            aSerializer.save()
            return Response(aSerializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(aSerializer.errors, status= status.HTTP_400_BAD_REQUEST)
    def put(self,request,pk = None):
        area = get_object_or_404(t_area, pk=pk)
        aSerializer = areaSerializer(area,data=request.data)
        if aSerializer.is_valid():
            aSerializer.save()
            return Response(aSerializer.data, status=status.HTTP_200_OK)
        else:
            return Response(aSerializer.errors, status= status.HTTP_400_BAD_REQUEST)
    def patch(self,request,pk = None):
        area = get_object_or_404(t_area, pk=pk)
        aSerializer = areaSerializer(area,data=request.data, partial = True)
        if aSerializer.is_valid():
            aSerializer.save()
            return Response(aSerializer.data, status=status.HTTP_200_OK)
        else:
            return Response(aSerializer.errors, status= status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk = None):
            area = get_object_or_404(t_area, pk=pk)
            area.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

class AreaListCreateView(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         GenericAPIView):
    queryset = t_area.objects.all()
    serializer_class = areaSerializer

    def get(self,request):
        return self.list(request)
    def post(self,request):
        return self.create(request)

class AreaDetailCreateView(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin, 
                           GenericAPIView):
    
    queryset = t_area.objects.all()
    serializer_class = areaSerializer

    def get(self,request, pk):
        return self.retrieve(request, pk=pk)
    def put(self,request, pk):
        return self.update(request, pk=pk)
    def patch(self, request, pk):
        return self.partial_update(request, pk=pk)
    def delete(self, request, pk):
        return self.destroy(request, pk=pk)

class listaViewSet(viewsets.ModelViewSet):
    queryset = t_lista.objects.all()
    serializer_class = listaSerializer

    @action(detail= True, methods=['get','post'])
    def desactivar(self, request, pk=None):
        t_lista = self.get_object()
        t_lista.nombre = 'DEFAULT'
        t_lista.save()
        return Response('Lista desactivada')

