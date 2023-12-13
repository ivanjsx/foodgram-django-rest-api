import re

from django.core.exceptions import ValidationError


def hex_color_validator(value):

    pattern = r"^#(?:[0-9a-fA-F]{3}){1,2}$"

    if not re.match(pattern, value):
        raise ValidationError(
            message="string must represent a valid hex color.",
            params={"value": value},
        )
