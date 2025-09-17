from django.utils.deprecation import MiddlewareMixin
from .utils.logging_utility import log_info, log_warning, log_error
import time

class AuthenticationLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        
        request._start_time = time.time()
        
        # Log request info
        if request.user.is_authenticated:
            log_info(f"Authenticated request: {request.method} {request.path} by user {request.user.username}")
        else:
            # Only log for API endpoints to avoid spam from static files
            if request.path.startswith('/api/'):
                log_info(f"Unauthenticated request: {request.method} {request.path}")
    
    def process_response(self, request, response):
        duration = time.time() - getattr(request, '_start_time', time.time())
        
        if request.path.startswith('/api/'):
            status_code = response.status_code
            user_info = request.user.username if request.user.is_authenticated else "Anonymous"
            
            log_message = f"Response: {status_code} for {request.method} {request.path} by {user_info} (Duration: {duration:.2f}s)"
            
            if status_code >= 400:
                if status_code == 403:
                    log_warning(f"Forbidden access: {log_message}")
                elif status_code == 404:
                    log_warning(f"Not found: {log_message}")
                else:
                    log_error(f"Error response: {log_message}")
            else:
                log_info(log_message)
        
        return response