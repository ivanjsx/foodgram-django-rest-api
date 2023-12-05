from django.contrib import admin

from .models import Favorite, Ingredient, Recipe, RecipeIngredient, Tag


class EmptyValueDisplay(admin.ModelAdmin):
    empty_value_display = "-empty-"


@admin.register(Tag)
class TagAdmin(EmptyValueDisplay):
    list_display = ("id", "name", "slug", "hex_color")
    search_fields = ("name", )


@admin.register(Ingredient)
class IngredientAdmin(EmptyValueDisplay):
    list_display = ("id", "name", "measurement_unit")
    search_fields = ("name", )


@admin.register(Favorite)
class FavoriteAdmin(EmptyValueDisplay):
    list_display = ("id", "user", "recipe")


@admin.register(Recipe)
class RecipeAdmin(EmptyValueDisplay):
    list_display = (
        "id", "name", "description", "cooking_time", "author", "cover_image",
        "tags", "ingredients"
    )
    list_filter = ("tags", "ingredients")
    list_editable = ("tags", )
    search_fields = ("name", )

    @admin.display(
        description='tags',
    )
    def tags(self, obj):
        return ', '.join(
            [tag.name for tag in obj.tags.all()]
        )

    @admin.display(
        description='ingredients',
    )
    def ingredients(self, obj):
        return ', '.join(
            # TODO indicate quantities as well
            [ingredient.name for ingredient in obj.ingredients.all()]
        )


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(EmptyValueDisplay):
    list_display = ("id", "recipe", "ingredient", "quantity")
