from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")

# Permitir lookup por slug o id
# DRF ya resuelve /posts/<pk>/, para slug puedes usar un CustomLookup si prefieres.
# Aquí usarás por defecto ID. Si quieres slug, define `lookup_field="slug"` en el ViewSet.

urlpatterns = router.urls
