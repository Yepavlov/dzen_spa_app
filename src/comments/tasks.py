from celery import shared_task
from PIL import Image

from config.settings import IMG_HEIGHT_LIMIT, IMG_WIDTH_LIMIT


@shared_task
def resize_image(comment_pk: int) -> None:
    """
    Background task for resizing an image.
    Accepts the primary key (pk) of the comment.
    """
    from .models import Comment

    try:
        comment = Comment.objects.get(pk=comment_pk)
        if comment.image:
            img = Image.open(comment.image.path)
            if img.height > IMG_HEIGHT_LIMIT or img.width > IMG_WIDTH_LIMIT:
                output_size = (IMG_WIDTH_LIMIT, IMG_HEIGHT_LIMIT)
                img.thumbnail(output_size)
                img.save(comment.image.path)
    except Comment.DoesNotExist:
        pass
