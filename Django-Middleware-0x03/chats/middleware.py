import logging
from datetime import datetime, timedelta
from rest_framework.exceptions import Throttled
from django.http import JsonResponse
from datetime import datetime, time
from django.http import HttpResponseForbidden

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

class RestrictAccessByTimeMiddleware:
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

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_data = {}  # Store: {ip: {"count": int, "start_time": datetime}}

    def __call__(self, request):
        ip_addr = request.META.get('REMOTE_ADDR', 'Unknown')

        now = datetime.now()
        ip_info = self.ip_data.get(ip_addr)
        endpoint = request.path

        try:
            if ip_info:
                # If the 1-minute window has passed, reset count and start time
                if (now - ip_info["start_time"]) > timedelta(minutes=1):
                    self.ip_data[ip_addr] = {"count": 1, "start_time": now}
                else:
                    ip_info["count"] += 1
                    if ip_info["count"] > 5 and ip_info["endpoint"] == request.path:
                        raise Throttled(detail="429 Too many requests, can't send more than 5 messages in 1 minute!")
            else:
                # First request from this IP
                self.ip_data[ip_addr] = {"count": 1, "start_time": now, 'endpoint': '/api/conversations/'}
        except Throttled as e:
            return JsonResponse(
                {"detail": str(e.detail)},
                status=e.status_code
            )

        return self.get_response(request)
        

        
