import json, time
from django.utils.deprecation import MiddlewareMixin

class JsonLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request._start_time = time.time()

    def process_response(self, request, response):
        try:
            elapsed = int((time.time() - getattr(request, "_start_time", time.time())) * 1000)
            log = {
                "method": request.method,
                "path": request.get_full_path(),
                "status": response.status_code,
                "elapsed_ms": elapsed,
            }
            # Opcional: loguear Authorization sin validar (para mañana conectar JWT)
            auth = request.META.get("HTTP_AUTHORIZATION")
            if auth:
                log["auth_header_present"] = True
                # Si quieres ver el valor exacto (cuidado en prod):
                # log["authorization"] = auth
            print(json.dumps(log))
        except Exception:
            pass
        return response
