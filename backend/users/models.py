from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models import (CASCADE, CharField, CheckConstraint, EmailField,
                              F, ForeignKey, Q, UniqueConstraint)

from core.models import WithTimestamps

from .constants import (ADMIN_USER_ROLE, DEFAULT_USER_ROLE, MAX_FIELD_LENGTH,
                        USER_ROLE_CHOICES)
from .validators import reserved_username_validator


class CustomUser(AbstractUser):
    """
    User model. Customized with respect to built-in model to disallow
    blank fields, validate against reserved usernames and define properties.
    """

    role = CharField(
        choices=USER_ROLE_CHOICES,
        default=DEFAULT_USER_ROLE,
        max_length=5,
    )
    first_name = CharField(
        verbose_name="first name",
        max_length=MAX_FIELD_LENGTH,
    )
    last_name = CharField(
        verbose_name="last name",
        max_length=MAX_FIELD_LENGTH
    )
    email = EmailField(
        verbose_name="email address",
        unique=True,
    )
    username = CharField(
        verbose_name="username",
        unique=True,
        max_length=MAX_FIELD_LENGTH,
        validators=(UnicodeUsernameValidator(), reserved_username_validator),
        error_messages={"unique": "user with this username already exists."},
    )

    class Meta(AbstractUser.Meta):
        ordering = ("username", )

    @property
    def recipes_count(self):
        return self.recipes.count()

    @property
    def is_admin(self):
        return self.role == ADMIN_USER_ROLE

    def __str__(self):
        return self.username


class Subscription(WithTimestamps):
    """
    Subscription (act of following) of a user to another user on the platform.
    """

    follower = ForeignKey(
        verbose_name="follower",
        to=CustomUser,
        on_delete=CASCADE,
        related_name="following",
    )
    influencer = ForeignKey(
        verbose_name="influencer",
        to=CustomUser,
        on_delete=CASCADE,
        related_name="followers",
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=("follower", "influencer"),
                name="already following this user"
            ),
            CheckConstraint(
                check=~Q(
                    follower=F("influencer")
                ),
                name="you cannot follow yourself",
            ),
        )

    def __str__(self):
        return f"{self.follower} follows {self.influencer}"
