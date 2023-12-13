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

