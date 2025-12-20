import logging

logger = logging.getLogger(__name__)

class AdminCsrfExemptMiddleware:
    """Отключает CSRF для админки"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            setattr(request, '_dont_enforce_csrf_checks', True)
        return self.get_response(request)


class RequestLoggingMiddleware:
    """Middleware для логирования всех входящих запросов"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Логируем входящий запрос
        print(f"=== REQUEST: {request.method} {request.path} ===")
        print(f"Headers: {dict(request.headers)}")
        print(f"Query params: {request.GET}")
        print(f"User agent: {request.META.get('HTTP_USER_AGENT', 'Unknown')}")
        print(f"User: {request.user}")
        print(f"Auth: {request.auth}")

        if request.method == 'OPTIONS':
            print("CORS preflight request detected")

        try:
            print("=== CALLING get_response ===")
            response = self.get_response(request)
            print("=== get_response completed ===")

            # Логируем ответ
            print(f"=== RESPONSE: {response.status_code} ===")
            print(f"Response headers: {dict(response.headers)}")

            return response

        except Exception as e:
            print(f"=== EXCEPTION in middleware: {str(e)} ===")
            import traceback
            print("=== FULL TRACEBACK ===")
            traceback.print_exc()
            print("=== END TRACEBACK ===")
            raise


class CORSMiddleware:
    """Добавляет CORS headers ко всем ответам"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Добавляем CORS headers для всех запросов
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        response['Access-Control-Max-Age'] = '86400'

        return response