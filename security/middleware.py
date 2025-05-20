import logging
from django.conf import settings
from django.http import HttpResponseForbidden

logger = logging.getLogger(__name__)

class SecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_ips = getattr(settings, 'ALLOWED_IPS', ['127.0.0.1'])

    def __call__(self, request):
        client_ip = request.META.get('REMOTE_ADDR')
        if client_ip not in self.allowed_ips:
            logger.warning(f"Blocked request from IP: {client_ip}")
            return HttpResponseForbidden("Access denied")
        
        response = self.get_response(request)
        return response
