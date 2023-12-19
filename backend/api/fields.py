import base64
import uuid

from django.core.files.base import ContentFile

from rest_framework.serializers import CharField, ImageField, ValidationError


class Base64ImageField(ImageField):
    """
    As an input for de-serialization, only accepts a base64-encoded image,
    and decodes it into a file suitable for ImageField.
    """

    def to_internal_value(self, data):

        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]
            file_name = f"{uuid.uuid4()}.{ext}"
            data = ContentFile(base64.b64decode(imgstr), name=file_name)

        return super().to_internal_value(data)


class StringToNaturalNumberField(CharField):
    """
    As an input for de-serialization, only accepts a string
    which can be successfully interpreted as a natural number.
    Primarily designed for the validation an type conversion
    of the query params that the API can potentially handle.
    """

    error_message = "must be a positive integer or 0"

    def to_internal_value(self, data):
        try:
            data = int(data)
        except ValueError:
            raise ValidationError(self.error_message)
        if data < 0:
            raise ValidationError(self.error_message)
        return data


class StringToBoolField(CharField):
    """
    As an input for de-serialization, only accepts two strings: `0` and `1`.
    Primarily designed for the validation an type conversion
    of the query params that the API can potentially handle.
    """

    error_message = "must be either 1 or 0"

    def to_internal_value(self, data):
        if data == "1":
            return True
        if data == "0":
            return False
        raise ValidationError(self.error_message)
