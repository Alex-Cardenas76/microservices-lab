from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework import viewsets, mixins, filters
from .models import Post
from .serializers import PostListSerializer, PostDetailSerializer

@method_decorator(cache_page(60), name="retrieve")  # detalle cacheado 60s
class PostViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.published().select_related("author","category")
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "body"]

    def get_serializer_class(self):
        return PostDetailSerializer if self.action == "retrieve" else PostListSerializer

    def retrieve(self, request, *args, **kwargs):
        # Contador de vistas simple (no se cachea el incremento porque responde desde caché)
        response = super().retrieve(request, *args, **kwargs)
        # (Opcional: mover a signal o a una vista sin caché si quieres exactitud)
        try:
            obj = self.get_object()
            type(self).queryset.model.objects.filter(pk=obj.pk).update(views=obj.views + 1)
        except Exception:
            pass
        return response
