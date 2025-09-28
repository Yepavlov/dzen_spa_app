from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User

from comments.utils.validators import validate_text_file_size


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    home_page = models.URLField(blank=True, null=True)
    text = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        upload_to="images/",
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "gif"])],
        blank=True,
        null=True,
    )
    text_file = models.FileField(
        upload_to="text_files/",
        validators=[FileExtensionValidator(allowed_extensions=["txt"]), validate_text_file_size],
        blank=True,
        null=True,
    )

    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.author.username} at {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new and self.image:
            from comments.tasks import resize_image

            resize_image.delay(self.pk)
