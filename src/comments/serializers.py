from typing import Any

from rest_framework import serializers
from captcha.models import CaptchaStore
from .models import Comment
import bleach


class CommentSerializer(serializers.ModelSerializer):
    ALLOWED_TAGS = {"a", "code", "i", "strong"}
    ALLOWED_ATTRIBUTES = {"a": ["href", "title"]}

    replies = serializers.SerializerMethodField()

    captcha_key = serializers.CharField(write_only=True, required=True)
    captcha_value = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "user_name",
            "email",
            "home_page",
            "text",
            "created_at",
            "parent",
            "replies",
            "image",
            "text_file",
            "captcha_key",
            "captcha_value",
        ]
        read_only_fields = ["id", "created_at", "replies"]

    def get_replies(self, obj: Comment) -> list[dict[str, Any]]:
        """
        Method for the 'replies' field to get all nested children.
        """
        queryset = Comment.objects.filter(parent=obj.id)
        serializer = self.__class__(queryset, many=True)
        return serializer.data

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        """Method for validating the CAPTCHA."""
        captcha_key = data.get("captcha_key")
        captcha_value = data.get("captcha_value", "").lower()

        try:
            store = CaptchaStore.objects.get(hashkey=captcha_key)
            if store.response != captcha_value:
                raise serializers.ValidationError("Incorrect CAPTCHA.")
            store.delete()
        except CaptchaStore.DoesNotExist:
            raise serializers.ValidationError("Invalid CAPTCHA key.")

        return super().validate(data)

    def create(self, validated_data: dict[str, Any]) -> Comment:
        """Method to remove CAPTCHA fields before saving the comment."""
        validated_data = self._clean_text_from_html(validated_data)
        validated_data.pop("captcha_key", None)
        validated_data.pop("captcha_value", None)
        return super().create(validated_data)

    def _clean_text_from_html(self, validated_data: dict[str, Any]) -> dict[str, Any]:
        """Cleans ‘text’ field from dangerous HTML."""
        validated_data["text"] = bleach.clean(
            validated_data["text"],
            tags=self.ALLOWED_TAGS,
            attributes=self.ALLOWED_ATTRIBUTES,
            strip=True,
        )
        return validated_data
