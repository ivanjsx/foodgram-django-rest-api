import base64
import uuid

from django.core.files.base import ContentFile

from rest_framework.serializers import CharField, ImageField, ValidationError


class StringToNaturalNumberField(CharField):

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

    error_message = "must be either 1 or 0"

    def to_internal_value(self, data):
        if data == "1":
            return True
        if data == "0":
            return False
        raise ValidationError(self.error_message)
