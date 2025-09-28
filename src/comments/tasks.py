import logging
from celery import shared_task
from PIL import Image
from django.core.files.storage import default_storage

from config.settings import IMG_HEIGHT_LIMIT, IMG_WIDTH_LIMIT

logger = logging.getLogger(__name__)


@shared_task
def resize_image(comment_pk: int) -> None:
    """
    Background task for resizing an image.
    Accepts the primary key (pk) of the comment.
    """
    from .models import Comment

    try:
        logger.info(f"Starting image resize task for comment {comment_pk}")

        comment = Comment.objects.get(pk=comment_pk)

        if not comment.image:
            logger.warning(f"Comment {comment_pk} has no image to resize")
            return

        if not default_storage.exists(comment.image.name):
            logger.error(f"Image file {comment.image.name} does not exist")
            return

        try:
            with Image.open(comment.image.path) as img:
                original_size = img.size
                if img.height > IMG_HEIGHT_LIMIT or img.width > IMG_WIDTH_LIMIT:
                    logger.info(
                        f"Resizing image for comment {comment_pk}: {original_size} -> "
                        f"max({IMG_WIDTH_LIMIT}, {IMG_HEIGHT_LIMIT})"
                    )

                    img.thumbnail((IMG_WIDTH_LIMIT, IMG_HEIGHT_LIMIT), Image.Resampling.LANCZOS)
                    img.save(comment.image.path, optimize=True, quality=85)

                    logger.info(
                        f"Successfully resized image for comment {comment_pk} from {original_size} to {img.size}"
                    )
                else:
                    logger.info(f"Image for comment {comment_pk} doesn't need resizing: {original_size}")

        except Exception as img_error:
            logger.error(f"Error processing image for comment {comment_pk}: {img_error}")

    except Comment.DoesNotExist:
        logger.error(f"Comment {comment_pk} does not exist")

    except Exception as exc:
        logger.error(f"Error in resize_image task for comment {comment_pk}: {exc}")
