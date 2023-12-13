from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db.models import (CASCADE, CharField, ForeignKey, ImageField,
                              IntegerField, ManyToManyField, Model,
                              PositiveSmallIntegerField, SlugField, TextField,
                              UniqueConstraint)

from core.models import WithTimestamps

from .constants import MAX_NAME_LENGTH, MAX_SLUG_LENGTH, MAX_UNIT_LENGTH
from .validators import hex_color_validator

User = get_user_model()


class WithName(Model):
    """
    Abstract model. Adds the `name` field to any successor, and orders
    instances with respect to it (unless explicitly specified otherwise).
    """

    name = CharField(
        max_length=MAX_NAME_LENGTH,
        verbose_name="name",
        help_text="Provide a name",
    )

    class Meta:
        abstract = True
        ordering = ("name", )

    def __str__(self):
        return self.name


class Tag(WithTimestamps, WithName):
    """
    A tag, which the recipe is tagged with.
    May be multiple thereof on a single recipe.
    """

    slug = SlugField(
        unique=True,
        max_length=MAX_SLUG_LENGTH,
        verbose_name="slug",
        help_text="Provide a unique slug (will be used in the URL address)",
    )
    color = CharField(
        unique=True,
        max_length=7,
        verbose_name="color",
        help_text="Provide a unique color",
        validators=(hex_color_validator, )
    )

    class Meta(WithName.Meta):
        constraints = (
            UniqueConstraint(
                fields=("name", ),
                name="tag name must be unique"
            ),
        )


class Ingredient(WithTimestamps, WithName):
    """
    An ingredient, which the recipe includes.
    Obligatory to include at least 1 in each recipe.
    """

    measurement_unit = CharField(
        max_length=MAX_UNIT_LENGTH,
        verbose_name="measurement unit",
        help_text="Provide a measurement unit",
    )

    class Meta(WithName.Meta):
        constraints = (
            UniqueConstraint(
                fields=("name", "measurement_unit"),
                name="name & measurement_unit must make a unique pair"
            ),
        )


class Recipe(WithTimestamps, WithName):
    """
    A recipe, the cornerstone for the app functionality.
    """

    text = TextField(
        verbose_name="description",
        help_text="Provide a description",
    )
    cooking_time = PositiveSmallIntegerField(
        verbose_name="Cooking time, in minutes",
        help_text="Provide a cooking, in minutes",
        validators=(MinValueValidator(1), )
    )
    author = ForeignKey(
        to=User,
        on_delete=CASCADE,
        verbose_name="author",
        related_name="recipes",
    )
    image = ImageField(
        upload_to="recipes/",
        verbose_name="Cover image",
        help_text="Upload a cover image",
    )
    tags = ManyToManyField(
        blank=True,
        to=Tag,
        through="RecipeTag",
        verbose_name="Set of tags",
        help_text="Provide a set of tags it belongs to",
    )

    class Meta:
        ordering = ("-created", )


class RecipeTag(WithTimestamps):
    """
    Implements Many-to-Many Relationship between a recipe and a tag.
    Defined explicitly for the sake of importing test data from CSV files.
    """

    recipe = ForeignKey(
        to=Recipe,
        editable=False,
        on_delete=CASCADE,
    )
    tag = ForeignKey(
        to=Tag,
        editable=False,
        on_delete=CASCADE,
        related_name="recipes",
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=("recipe", "tag"),
                name="recipe & tag must make a unique pair"
            ),
        )

    def __str__(self):
        return f"{self.recipe} is tagged with {self.tag}"


class Amount(WithTimestamps):
    """
    Implements Many-to-Many Relationship between a recipe and an ingredient.
    Defined explicitly to indicate additional data (for instance, amount).
    """

    recipe = ForeignKey(
        to=Recipe,
        editable=False,
        on_delete=CASCADE,
        related_name="ingredients",
    )
    ingredient = ForeignKey(
        to=Ingredient,
        editable=False,
        on_delete=CASCADE,
        related_name="recipes",
    )
    amount = IntegerField(
        verbose_name="amount",
        help_text="Provide the amount needed",
        validators=(MinValueValidator(1), )
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=("recipe", "ingredient"),
                name="recipe & ingredient must make a unique pair"
            ),
        )

    def __str__(self):
        return f"{self.recipe} includes {self.amount} of {self.ingredient}"


class Favorite(WithTimestamps):
    """
    Lets users add recipes to their Favorites list.
    """

    user = ForeignKey(
        to=User,
        editable=False,
        on_delete=CASCADE,
        related_name="favorites",
    )
    recipe = ForeignKey(
        to=Recipe,
        editable=False,
        on_delete=CASCADE,
        related_name="in_favorites",
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=("user", "recipe"),
                name="already in favorites"
            ),
        )

    def __str__(self):
        return f"{self.user} has {self.recipe} in their favorites"


class Cart(WithTimestamps):
    """
    Lets users add recipes to their Shopping Cart list.
    """

    user = ForeignKey(
        to=User,
        editable=False,
        on_delete=CASCADE,
        related_name="cart",
    )
    recipe = ForeignKey(
        to=Recipe,
        editable=False,
        on_delete=CASCADE,
        related_name="in_cart",
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=("user", "recipe"),
                name="already in shopping cart"
            ),
        )

    def __str__(self):
        return f"{self.user} has {self.recipe} in their shopping cart"
