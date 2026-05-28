from functools import wraps
from django.http import HttpResponseForbidden


def rol_requerido(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_superuser or request.user.rol in roles:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
        return wrapper
    return decorator
