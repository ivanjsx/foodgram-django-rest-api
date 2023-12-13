from django_filters.rest_framework import (AllValuesMultipleFilter, CharFilter,
                                           FilterSet, NumberFilter)

from django.db.models import OuterRef, Subquery

from recipes.models import Cart, Favorite, Ingredient, Recipe


class FilterIngredientsByName(FilterSet):
    """
    Custom filter implementation for Ingredient model viewset.
    """

    name = CharFilter(lookup_expr="istartswith")

    class Meta:
        model = Ingredient
        fields = ("name", )


class FilterRecipesByTagsAndAuthor(FilterSet):
    """
    Custom filter implementation for Recipe model viewset.
    """

    tags = AllValuesMultipleFilter(field_name="tags__slug")
    author = NumberFilter(field_name="author__id", lookup_expr="exact")

    class Meta:
        model = Recipe
        fields = ("tags", "author")

