from rest_framework import viewsets
from .models import Comment
from .serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows to view and edit comments.
    """

    serializer_class = CommentSerializer
    queryset = Comment.objects.filter(parent__isnull=True)
