from typing import Any

from rest_framework import serializers
from captcha.models import CaptchaStore
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
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

    def validate(self, data: dict):
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

    def create(self, validated_data):
        """Method to remove CAPTCHA fields before saving the comment."""
        validated_data.pop("captcha_key", None)
        validated_data.pop("captcha_value", None)
        return super().create(validated_data)
