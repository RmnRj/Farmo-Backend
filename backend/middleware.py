from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger('django.security')


class SecurityLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            logger.info(f'{request.method} {request.path} from {self.get_client_ip(request)}')
        return None

    def process_response(self, request, response):
        if response.status_code >= 400:
            logger.warning(f'{request.method} {request.path} - Status: {response.status_code}')
        return response

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
