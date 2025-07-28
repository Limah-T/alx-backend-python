import logging
from datetime import datetime

logger = logging.getLogger(__name__) # Get a logger instance for the current module; in this case "middleware.py"

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        # One-time configuration/initialization
        self.get_response = get_response
    
    def __call__(self, request):
        # The code here will execute before calling the view
        print("Start")
        user = request.user
        logging.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        # The code here will execute after calling the view
        response = self.get_response(request)
        print("Done!")
        return response