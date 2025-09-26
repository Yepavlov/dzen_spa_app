from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile

from config.settings import FILE_SIZE_LIMIT


def validate_text_file_size(value: UploadedFile) -> None:
    """Validate that the uploaded file size does not exceed the limit."""
    if value.size > FILE_SIZE_LIMIT:
        raise ValidationError("The file is too large. The size must not exceed 100 KB.")
