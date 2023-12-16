from django_filters.rest_framework import (CharFilter, FilterSet,
                                           ModelMultipleChoiceFilter,
                                           NumberFilter)

from django.db.models import OuterRef, Subquery

from recipes.models import CartItem, FavoriteItem, Ingredient, Recipe, Tag


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

    author = NumberFilter(field_name="author__id", lookup_expr="exact")
    tags = ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name="tags__slug",
        to_field_name="slug",
    )

    class Meta:
        model = Recipe
        fields = ("tags", "author")


def filter_recipes_by_query_params(queryset, user, params):

    def subquery(list_model, user):
        if user.is_authenticated:
            return Subquery(
                list_model.objects.filter(
                    user=user, recipe=OuterRef("pk")
                ).values_list(
                    "recipe", flat=True
                )
            )
        return list_model.objects.none()

    def inner_join(queryset, subquery):
        return queryset.filter(
            id__in=subquery
        )

    def outer_join(queryset, subquery):
        return queryset.exclude(
            id__in=subquery
        )

    if params.get("is_favorited", None) is True:
        queryset = inner_join(queryset, subquery(FavoriteItem, user))

    if params.get("is_favorited", None) is False:
        queryset = outer_join(queryset, subquery(FavoriteItem, user))

    if params.get("is_in_shopping_cart", None) is True:
        queryset = inner_join(queryset, subquery(CartItem, user))

    if params.get("is_in_shopping_cart", None) is False:
        return outer_join(queryset, subquery(CartItem, user))

    return queryset
