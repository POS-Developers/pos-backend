from rest_framework.views import APIView
from Pos_Main_App.models import Dishes_model, Bill_model,  Employe_model,Table_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets


from Pos_Main_App.api.serializers   import Dishes_Serializer, Employe_Serializer, Bill_Serializer,  Table_Serializer
from Pos_Main_App.api.filters import Dishes_filter, Bill_filter, Employe_filter, Table_filter

from django.views.decorators.csrf import csrf_exempt



class Dishes_View(generics.ListCreateAPIView):
    queryset = Dishes_model.objects.all()
    serializer_class= Dishes_Serializer
    filter_backends= [DjangoFilterBackend]
    filterset_class= Dishes_filter



class Dishes_Details_View(generics.RetrieveUpdateDestroyAPIView):
    queryset= Dishes_model.objects.all()
    serializer_class= Dishes_Serializer




class Bill_View(generics.ListCreateAPIView):
    queryset = Bill_model.objects.all()
    serializer_class= Bill_Serializer
    filter_backends= [DjangoFilterBackend]
    filterset_class=Bill_filter



class Bill_Details_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bill_model.objects.all()
    serializer_class = Bill_Serializer   



class Employe_View(generics.ListCreateAPIView):
    queryset = Employe_model.objects.all()
    serializer_class= Employe_Serializer
    filter_backends= [DjangoFilterBackend]
    filterset_class= Employe_filter


class Employe_Details_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employe_model.objects.all()
    serializer_class = Employe_Serializer




class Table_View(generics.ListCreateAPIView):
    queryset = Table_model.objects.all()
    serializer_class= Table_Serializer
    filter_backends= [DjangoFilterBackend]
    filterset_class= Table_filter


class Bill_View(generics.ListCreateAPIView):
    queryset = Bill_model.objects.all()
    serializer_class= Bill_Serializer
    filter_backends= [DjangoFilterBackend]
    filterset_class=Bill_filter



class Bill_Details_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bill_model.objects.all()
    serializer_class = Bill_Serializer   





