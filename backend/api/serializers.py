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


class QueryParamsSerializer(Serializer):

    pk = StringToNaturalNumberField(required=False)
    is_favorited = StringToBoolField(required=False)
    is_in_shopping_cart = StringToBoolField(required=False)
    recipes_limit = StringToNaturalNumberField(required=False)

    class Meta:
        fields = ("pk", "is_favorited", "is_in_shopping_cart", "recipes_limit")


class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class IngredientSerializer(ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")



class UserShowSerializer(ModelSerializer):

    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = ("email", "id", "username", "first_name", "last_name",
                  "is_subscribed")

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        if not user.is_authenticated:
            return False
        return user.following.filter(influencer=obj).exists()



class UserCreateSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ("email", "id", "username", "first_name", "last_name",
                  "password")
        extra_kwargs = {"password": {"required": True, "write_only": True}}

    def validate_password(self, value):
        password_validation.validate_password(value,
                                              self.context["request"].user)
        return value

