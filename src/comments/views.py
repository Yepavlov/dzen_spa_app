import logging
from django.core.cache import cache
from rest_framework import viewsets, response
from .models import Comment
from .serializers import CommentSerializer

logger = logging.getLogger(__name__)


class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows to view and edit comments.
    """

    serializer_class = CommentSerializer
    queryset = Comment.objects.filter(parent__isnull=True)

    def list(self, request, *arg, **kwargs):
        cache_key = "comment_list"
        cached_data = cache.get(cache_key)

        if cached_data:
            logger.info(f"'{cache_key}' found in cache. Serving from cache.")
            return response.Response(cached_data)

        logger.info(f"'{cache_key}' not found in cache. Querying database.")
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        cache.set(cache_key, data, timeout=60 * 5)

        return response.Response(data)
