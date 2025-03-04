import traceback
from django.http import JsonResponse
from .api.utils import send_slack_error_message  # Import the function

class SlackErrorMiddleware:
    """Middleware to catch all exceptions and send error messages to Slack."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            error_message = traceback.format_exc()  # Get full error traceback
            send_slack_error_message(error_message)  # Send error to Slack
            
            return JsonResponse(
                {"error": "An unexpected error occurred."}, 
                status=500
            )
