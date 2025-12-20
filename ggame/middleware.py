"""
Middleware для обхода CSRF в админке Railway
"""
from django.utils.deprecation import MiddlewareMixin


class AdminCsrfExemptMiddleware(MiddlewareMixin):
    """
    Отключает CSRF проверку для админки
    """

    def process_view(self, request, callback, callback_args, callback_kwargs):
        """
        Отключает CSRF для URL начинающихся с /admin/
        """
        if request.path.startswith('/admin/'):
            # Отключаем CSRF проверку
            setattr(request, '_dont_enforce_csrf_checks', True)

        return None
