from django.contrib.auth import get_user_model, password_validation
from django.shortcuts import get_object_or_404

from rest_framework.serializers import (CharField, IntegerField,
                                        ModelSerializer,
                                        PrimaryKeyRelatedField, Serializer,
                                        SerializerMethodField, ValidationError)

from recipes.models import Amount, Ingredient, Recipe, RecipeTag, Tag

from .fields import (Base64ImageField, StringToBoolField,
                     StringToNaturalNumberField)

User = get_user_model()



class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class IngredientSerializer(ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


