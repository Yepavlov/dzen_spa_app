from django.db import models


class Comment(models.Model):
    user_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    home_page = models.URLField(blank=True, null=True)
    text = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.user_name} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"
