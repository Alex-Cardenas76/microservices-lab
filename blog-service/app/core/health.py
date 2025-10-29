from django.db import connections
from django.http import JsonResponse
from django.core.cache import cache
import time

def healthz(request):
    started = time.time()
    # DB check
    with connections["default"].cursor() as c:
        c.execute("SELECT 1;")
        db_ok = c.fetchone() == (1,)

    # Redis check
    try:
        cache.set("healthz", "ok", 5)
        redis_ok = cache.get("healthz") == "ok"
    except Exception:
        redis_ok = False

    return JsonResponse({
        "db": "ok" if db_ok else "fail",
        "redis": "ok" if redis_ok else "fail",
        "elapsed_ms": int((time.time() - started)*1000),
    }, status=200 if db_ok and redis_ok else 503)
    