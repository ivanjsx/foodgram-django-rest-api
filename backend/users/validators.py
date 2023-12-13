from django.core.exceptions import ValidationError

from .constants import RESERVED_USERNAMES


def reserved_username_validator(value):

    if value.lower() in RESERVED_USERNAMES:
        raise ValidationError(
            message="This username is reserved and cannot be used.",
            params={"value": value},
        )
