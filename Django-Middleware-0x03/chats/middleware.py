import logging
from datetime import datetime

logger = logging.getLogger(__name__) # Get a logger instance for the current module; in this case "middleware.py"

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        # One-time configuration/initialization
        self.get_response = get_response
    
    def __call__(self, request):
        # The code here will execute before calling the view
        user = request.user
        logging.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        # The code here will execute after calling the view
        response = self.get_response(request)
        return response
    
# messaging/middleware.py
from datetime import datetime, time
from django.http import HttpResponseForbidden

class RestrictMessagingHoursMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # The code here will execute before calling the view
        user = request.user
        logging.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        # The code here will execute after calling the view
        # Define access hours
        start_time = time(18, 0)   # 6:00 PM
        end_time = time(21, 0)    # 9:00 PM

        # Check if the request path is for the messaging app
        if request.path.startswith('/conversations/'): 
            now = datetime.now().time()
            if not (self.start_time <= now <= self.end_time):
                return HttpResponseForbidden("403 Forbidden: Access to chats is only allowed between 6 PM and 9 PM.")

        response = self.get_response(request)
        return response
