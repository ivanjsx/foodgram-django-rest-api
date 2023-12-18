from django.contrib import admin
from django.forms import BaseInlineFormSet, ValidationError

from .models import (CartItem, FavoriteItem, Ingredient,
                     IngredientAmountInRecipe, Recipe, RecipeTag, Tag)

admin.site.empty_value_display = "-empty-"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "color")
    search_fields = ("name", "slug")
    list_filter = ("name", )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "measurement_unit")
    search_fields = ("name", )
    list_filter = ("name", )


@admin.register(FavoriteItem)
class FavoriteItemAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "recipe")


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "recipe")


class RequiredInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        objects_count = 0
        for form in self.forms:
            if form.cleaned_data:
                objects_count += 1

        if objects_count < 1:
            raise ValidationError("At least one related object is required.")


class RecipeTagInline(admin.TabularInline):
    model = RecipeTag
    formset = RequiredInlineFormSet
    min_num = 1


class AmountInline(admin.TabularInline):
    model = IngredientAmountInRecipe
    formset = RequiredInlineFormSet
    min_num = 1


@admin.display(description="tags")
def tags(obj):
    return ", ".join(
        obj.tags.all().values_list("name", flat=True)
    )


@admin.display(description="ingredients")
def ingredients(obj):
    return ", ".join(
        obj.ingredients.all().values_list("ingredient__name", flat=True)
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name", "cooking_time", "author", "image",
        tags, ingredients, "times_favorited"
    )
    list_filter = ("tags", "author", "name")
    search_fields = ("name", )
    inlines = (RecipeTagInline, AmountInline)
