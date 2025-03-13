from rest_framework.views import APIView
from Pos_Main_App.models import Dishes_model, Bill_model, OrderedDish_model, Employe_model, Table_model, ContactSupport
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from Pos_Main_App.api.serializers import (
    Dishes_Serializer, Employe_Serializer, Bill_Serializer, OrderedDish_Serializer, Table_Serializer, ContactSupportSerializer
)
from Pos_Main_App.api.filters import Dishes_filter, OrderedDish_filter, Bill_filter, Employe_filter, Table_filter
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import send_slack_error_message, send_slack_notification
from rest_framework.response import Response
from rest_framework import status
import traceback

def health_check(request):
    return JsonResponse({"status": "OK"})

def api_data(request):
    if request.method == 'GET':
        return JsonResponse({"message": "Hello from the backend!", "status": "success"})
    return JsonResponse({"error": "Method not allowed"}, status=405)

class Dishes_View(generics.ListCreateAPIView):
    queryset = Dishes_model.objects.all()
    serializer_class = Dishes_Serializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = Dishes_filter

class Dishes_Details_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dishes_model.objects.all()
    serializer_class = Dishes_Serializer

class Bill_View(generics.ListCreateAPIView):
    queryset = Bill_model.objects.all()
    serializer_class = Bill_Serializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = Bill_filter

class Bill_Details_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bill_model.objects.all()
    serializer_class = Bill_Serializer

class Employe_View(generics.ListCreateAPIView):
    queryset = Employe_model.objects.all()
    serializer_class = Employe_Serializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = Employe_filter

class Employe_Details_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employe_model.objects.all()
    serializer_class = Employe_Serializer

class Table_View(generics.ListCreateAPIView):
    queryset = Table_model.objects.all()
    serializer_class = Table_Serializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = Table_filter

def test_slack_error(request):
    """View to trigger an error and send a Slack message."""
    try:
        1 / 0  # Intentional ZeroDivisionError
    except Exception as e:
        error_message = traceback.format_exc()
        send_slack_error_message(error_message)
        return JsonResponse({"error": "An error occurred. Check Slack."}, status=500)

@csrf_exempt
class ContactSupportView(APIView):
    def get(self, request, *args, **kwargs):
        contacts = ContactSupport.objects.all()
        serializer = ContactSupportSerializer(contacts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        try:
            serializer = ContactSupportSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Contact request submitted successfully!"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_message = traceback.format_exc()
            send_slack_notification(error_message, request)
            return Response({"error": "An internal server error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
