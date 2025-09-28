import logging

from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.core.cache import cache
from django.http import JsonResponse
from rest_framework import viewsets, response
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Comment
from .serializers import CommentSerializer

logger = logging.getLogger(__name__)


class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows to view and edit comments.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer
    queryset = Comment.objects.filter(parent__isnull=True)

    filter_backends = [OrderingFilter]
    ordering_fields = ["author__username", "author__email", "created_at"]

    def list(self, request, *arg, **kwargs):
        page = request.query_params.get("page", "1")
        ordering = request.query_params.get("ordering", "-created_at")
        cache_key = f"comment_list_page_{page}_ordering_{ordering}"

        cached_data = cache.get(cache_key)

        if cached_data:
            logger.info(f"'{cache_key}' found in cache. Serving from cache.")
            return response.Response(cached_data)

        logger.info(f"'{cache_key}' not found in cache. Querying database.")
        return super().list(request, *arg, **kwargs)


def get_captcha(request):
    key = CaptchaStore.generate_key()
    image_url = captcha_image_url(key)
    return JsonResponse({"key": key, "image_url": image_url})
