from django.contrib import admin

from .models import Favorite, Ingredient, Recipe, RecipeIngredient, Tag


class EmptyValueDisplay(admin.ModelAdmin):
    empty_value_display = "-empty-"


@admin.register(Tag)
class TagAdmin(EmptyValueDisplay):
    list_display = ("id", "title", "slug", "hex_color")
    search_fields = ("title", )


@admin.register(Ingredient)
class IngredientAdmin(EmptyValueDisplay):
    list_display = ("id", "title", "measurement_unit")
    search_fields = ("title", )


@admin.register(Favorite)
class FavoriteAdmin(EmptyValueDisplay):
    list_display = ("id", "user", "recipe")


@admin.register(Recipe)
class RecipeAdmin(EmptyValueDisplay):
    list_display = (
        "id", "title", "description", "cooking_time", "author", "cover_image",
        "tags", "ingredients"
    )
    list_filter = ("tags", "ingredients")
    list_editable = ("tags", )
    search_fields = ("title", )

    @admin.display(
        description='tags',
    )
    def tags(self, obj):
        return ', '.join(
            [tag.title for tag in obj.tags.all()]
        )

    @admin.display(
        description='ingredients',
    )
    def ingredients(self, obj):
        return ', '.join(
            # TODO indicate quantities as well
            [ingredient.title for ingredient in obj.ingredients.all()]
        )


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(EmptyValueDisplay):
    list_display = ("id", "recipe", "ingredient", "quantity")
