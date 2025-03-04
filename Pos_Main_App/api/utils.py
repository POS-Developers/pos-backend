import requests
import json
import traceback
import logging
from django.conf import settings

def send_slack_error_message(error_message):
    """Send formatted error logs to Slack via Webhook."""
    if not settings.SLACK_WEBHOOK_URL:
        logging.warning("Slack webhook URL is not set. Skipping Slack notification.")
        return  # Skip if webhook URL is not set

    slack_data = {"text": f"🚨 *ERROR ALERT* 🚨\n```{error_message}```"}
    
    try:
        response = requests.post(
            settings.SLACK_WEBHOOK_URL, 
            data=json.dumps(slack_data), 
            headers={"Content-Type": "application/json"}
        )

        if response.status_code != 200:
            logging.error(f"Slack notification failed: {response.text}")
    except Exception as e:
        error_traceback = traceback.format_exc()  # Capture full traceback
        logging.error(f"Failed to send Slack message: {error_traceback}")


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import send_slack_error_message
from Pos_Main_App.api.serializers import ContactSupportSerializer

class ContactSupportView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ContactSupportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Contact request submitted successfully!"}, status=status.HTTP_201_CREATED)
        
        # Log error to Slack if request fails
        error_message = f"ContactSupport API Error: {serializer.errors}"
        logging.error(error_message)
        send_slack_error_message(error_message)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
