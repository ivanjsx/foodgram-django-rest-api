from django.contrib.auth import get_user_model
from django.db.models import (
    CheckConstraint, CASCADE, F, ForeignKey, Q, UniqueConstraint
)

from core.models import WithTimestamps

User = get_user_model()


class Follow(WithTimestamps):
    """
    Subscription of a user to another user on the platform.
    """

    follower = ForeignKey(
        to=User,
        editable=False,
        on_delete=CASCADE,
        related_name="following",
        verbose_name="follower",
    )
    influencer = ForeignKey(
        to=User,
        editable=False,
        on_delete=CASCADE,
        related_name="followers",
        verbose_name="influencer",
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=["follower", "influencer"],
                name="follower & influencer must make a unique pair",
            ),
            CheckConstraint(
                check=~Q(
                    follower=F("influencer")
                ),
                name="cannot follow yourself",
            ),
        )

    def __str__(self) -> str:
        return f"{self.follower} follows {self.influencer}"
