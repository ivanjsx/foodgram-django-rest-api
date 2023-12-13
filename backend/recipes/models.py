from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db.models import (
    CASCADE, CharField, FloatField, ForeignKey, ImageField, ManyToManyField,
    Model, PositiveSmallIntegerField, SlugField, TextField, UniqueConstraint,
)

from core.models import WithTimestamps

from .constants import MAX_TITLE_LENGTH, MAX_UNIT_LENGTH

User = get_user_model()


class WithTitle(Model):
    name = CharField(
        max_length=MAX_TITLE_LENGTH,
        verbose_name="name",
        help_text="Provide a name",
    )

    class Meta:
        abstract = True
        ordering = ("name", )

    def __str__(self):
        return self.name


class Tag(WithTimestamps, WithTitle):
    """
    A tag, which the recipe may or may not be tagged with.
    """

    slug = SlugField(
        unique=True,
        verbose_name="slug",
        help_text="Provide a unique slug (will be used in the URL address)",
    )
    hex_color = ColorField(
        unique=True,
        default="#FF0000",
        verbose_name="color",
        help_text="Provide a unique color",
    )

    class Meta(WithTitle.Meta):
        default_related_name = "tags"
        constraints = (
            UniqueConstraint(
                fields=("name", ),
                name="tag name must be unique"
            ),
        )


class Ingredient(WithTimestamps, WithTitle):
    """
    An ingredient, which the recipe includes.
    """

    measurement_unit = CharField(
        max_length=MAX_UNIT_LENGTH,
        verbose_name="measurement unit",
        help_text="Provide a measurement unit",
    )

    class Meta(WithTitle.Meta):
        default_related_name = "ingredients"
        constraints = (
            UniqueConstraint(
                fields=("name", "measurement_unit"),
                name="name & measurement_unit must make a unique pair"
            ),
        )


class Recipe(WithTimestamps, WithTitle):
    """
    A recipe, the cornerstone for the app functionality.
    """

    description = TextField(
        verbose_name="description",
        help_text="Provide a description",
    )
    cooking_time = PositiveSmallIntegerField(
        verbose_name="Cooking time, in minutes",
        help_text="Provide a cooking, in minutes",
    )
    author = ForeignKey(
        to=User,
        on_delete=CASCADE,
        verbose_name="author",
    )
    cover_image = ImageField(
        upload_to="recipes/",
        verbose_name="Cover image",
        help_text="Upload a cover image",
    )
    ingredients = ManyToManyField(
        to=Ingredient,
        through="Quantity",
        verbose_name="Set of ingredients",
        help_text="Provide a set of ingredients it includes",
    )
    tags = ManyToManyField(
        blank=True,
        to=Tag,
        through="RecipeTag",
        verbose_name="Set of tags",
        help_text="Provide a set of tags it belongs to",
    )

    class Meta(WithTitle.Meta):
        default_related_name = "recipes"
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


class Quantity(WithTimestamps):
    """
    Implements Many-to-Many Relationship between a recipe and an ingredient.
    Defined explicitly to indicate additional data (like quantity).
    """

    recipe = ForeignKey(
        to=Recipe,
        editable=False,
        on_delete=CASCADE,
    )
    ingredient = ForeignKey(
        to=Ingredient,
        editable=False,
        on_delete=CASCADE,
    )
    quantity = FloatField(
        verbose_name="quantity",
        help_text="Provide a quantity needed",
    )

    class Meta:
        verbose_name_plural = "Quantities"
        constraints = (
            UniqueConstraint(
                fields=("recipe", "ingredient"),
                name="recipe & ingredient must make a unique pair"
            ),
        )

    def __str__(self):
        return f"{self.recipe} includes {self.quantity} of {self.ingredient}"


class Favorite(WithTimestamps):
    """
    Lets users add recipes to their Favorites list
    """

    user = ForeignKey(
        to=User,
        editable=False,
        on_delete=CASCADE,
    )
    recipe = ForeignKey(
        to=Recipe,
        editable=False,
        on_delete=CASCADE,
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=("user", "recipe"),
                name="user & recipe must make a unique pair"
            ),
        )

    def __str__(self):
        return f"{self.user} has saved {self.recipe} in their favorites"