"""users app constants."""


MAX_FIELD_LENGTH = 150

RESERVED_USERNAMES = (
    "me",
    "admin",
    "superuser",
    "set_password",
    "subscriptions",
)

ADMIN_USER_ROLE = "admin"
DEFAULT_USER_ROLE = "user"
USER_ROLE_CHOICES = (
    ("admin", "Admin"),
    ("user", "User"),
)
