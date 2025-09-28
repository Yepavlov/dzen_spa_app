from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import Comment
from .serializers import CommentDetailSerializer


@receiver(post_save, sender=Comment)
def comment_handler(sender, instance, created, **kwargs):
    """Clears the 'comment_list' cache whenever a new comment is created."""
    if created:
        cache.delete_pattern("comment_list_*")
        channel_layer = get_channel_layer()
        serializer = CommentDetailSerializer(instance)

        async_to_sync(channel_layer.group_send)("comments", {"type": "comment.message", "message": serializer.data})
