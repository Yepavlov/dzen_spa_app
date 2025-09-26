from django.core.validators import FileExtensionValidator
from django.db import models

from comments.utils.validators import validate_text_file_size
from config.celery import app as celery_app


class Comment(models.Model):
    user_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
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
        return f"Comment by {self.user_name} at {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new and self.image:
            celery_app.send_task("comments.tasks.resize_image", args=[self.pk])
