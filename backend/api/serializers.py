from django.contrib.auth import password_validation
from django.shortcuts import get_object_or_404

from rest_framework.serializers import (CharField, IntegerField,
                                        ModelSerializer,
                                        PrimaryKeyRelatedField, Serializer,
                                        SerializerMethodField, ValidationError)

from recipes.models import (Ingredient, IngredientAmountInRecipe, Recipe,
                            RecipeTag, Tag)
from users.models import CustomUser as User

from .fields import (Base64ImageField, StringToBoolField,
                     StringToNaturalNumberField)


class QueryParamsSerializer(Serializer):
    """
    A single entry point for the validation and type conversion
    of all the query params that the API can potentially handle.
    Typical usage example:

    param_value = request.query_params.get("param_name", None)
    if param_value:
        serializer = QueryParamsSerializer(data={"param_name": param_value})
        serializer.is_valid(raise_exception=True)
        validated_param_value = serializer.validated_data["param_name"]
        do_something(validated_param_value)

    """

    pk = StringToNaturalNumberField(required=False)
    is_favorited = StringToBoolField(required=False)
    is_in_shopping_cart = StringToBoolField(required=False)
    recipes_limit = StringToNaturalNumberField(required=False)


class TagSerializer(ModelSerializer):
    """
    Serializes and de-serializes Tag model instances.
    """

    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class IngredientSerializer(ModelSerializer):
    """
    Serializes and de-serializes Ingredient model instances.
    """

    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class UserShowSerializer(ModelSerializer):
    """
    Serializes User model instances.
    Only designed for displaying an already-existing model instance
    within the body of the response which replies to safe-methods request.
    """

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


class ExtendedUserShowSerializer(UserShowSerializer):
    """
    Just a usual UserShowSerializer, with 2 additional fields introduced:
    `recipes` and `recipes_count`.
    """

    recipes = SerializerMethodField()

    class Meta(UserShowSerializer.Meta):
        fields = ("email", "id", "username", "first_name", "last_name",
                  "is_subscribed", "recipes", "recipes_count")

    def get_recipes(self, obj):
        recipes = obj.recipes.all()
        limit = self.context["request"].query_params.get("recipes_limit", None)
        if limit:
            serializer = QueryParamsSerializer(data={"recipes_limit": limit})
            serializer.is_valid(raise_exception=True)
            validated_limit = serializer.validated_data["recipes_limit"]
            recipes = recipes[:validated_limit]
        serializer = MinifiedRecipeSerializer(
            instance=recipes, many=True, read_only=True
        )
        return serializer.data


class UserCreateSerializer(ModelSerializer):
    """
    De-serializes User model instances.
    Only designed for converting the data provided in unsafe-methods request
    to internal database value, and displaying back the newly created object
    within the response body.
    """

    class Meta:
        model = User
        fields = ("email", "id", "username", "first_name", "last_name",
                  "password")
        extra_kwargs = {"password": {"required": True, "write_only": True}}

    def validate_password(self, value):
        password_validation.validate_password(value,
                                              self.context["request"].user)
        return value


class ChangePasswordSerializer(Serializer):
    """
    De-serializes data provided within the body
    of a request to change user's password.
    """

    current_password = CharField(required=True)
    new_password = CharField(required=True)

    def validate_current_password(self, value):
        user = self.context["user"]
        if not user.check_password(value):
            raise ValidationError(
                "your current password is incorrect"
            )
        return value

    def validate_new_password(self, value):
        password_validation.validate_password(
            value, self.context["user"]
        )
        return value

    def validate(self, data):
        if data["new_password"] == data["current_password"]:
            raise ValidationError(
                "your new password shall differ from current"
            )
        return data


class AmountInputSerializer(Serializer):
    """
    De-serializes data provided within the `ingredients` list field
    upon creating or modifying a Recipe model instance.
    """

    id = IntegerField()
    amount = IntegerField(write_only=True, min_value=1)

    def validate_id(self, value):
        if not Ingredient.objects.filter(id=value).exists():
            raise ValidationError("ingredient with provided id does not exist")
        return value


class AmountOutputSerializer(ModelSerializer):
    """
    Serializes `ingredients` list on an already-existing Recipe instance.
    """

    id = IntegerField(source="ingredient.id")
    name = CharField(source="ingredient.name")
    measurement_unit = CharField(source="ingredient.measurement_unit")

    class Meta:
        model = IngredientAmountInRecipe
        fields = ("id", "name", "measurement_unit", "amount")


class DefaultRecipeSerializer(ModelSerializer):
    """
    Serializes and de-serializes Recipe model instances.
    """

    author = UserShowSerializer(required=False)
    image = Base64ImageField()
    ingredients = AmountInputSerializer(many=True)
    tags = PrimaryKeyRelatedField(many=True,
                                  queryset=Tag.objects.all())
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ("id", "name", "text", "cooking_time", "author", "image",
                  "tags", "ingredients", "is_favorited", "is_in_shopping_cart")

    def validate_tags(self, value):
        if len(value) == 0:
            raise ValidationError("recipe requires at least 1 tag")
        if len(value) != len(set(value)):
            raise ValidationError("cannot assign multiple identical tags")
        return value

    def validate_ingredients(self, value):
        if len(value) == 0:
            raise ValidationError("recipe requires at least 1 ingredient")
        if len(value) != len({item["id"] for item in value}):
            raise ValidationError("cannot add multiple identical ingredients")
        return value

    def get_is_favorited(self, obj):
        user = self.context["request"].user
        if not user.is_authenticated:
            return False
        return user.favorite.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context["request"].user
        if not user.is_authenticated:
            return False
        return user.cart.filter(recipe=obj).exists()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        ingredients = AmountOutputSerializer(
            instance=instance.ingredients.all(),
            many=True
        )
        tags = TagSerializer(
            instance=instance.tags.all(),
            many=True
        )
        representation["ingredients"] = ingredients.data
        representation["tags"] = tags.data
        representation["image"] = instance.image.url
        return representation

    def create(self, validated_data):
        tags = validated_data.pop("tags", [])
        ingredients = validated_data.pop("ingredients", [])
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            RecipeTag.objects.create(recipe=recipe, tag=tag)
        for data in ingredients:
            ingredient = get_object_or_404(Ingredient, id=data["id"])
            IngredientAmountInRecipe.objects.create(recipe=recipe,
                                                    ingredient=ingredient,
                                                    amount=data["amount"])
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)
        ingredients = validated_data.pop("ingredients", None)
        instance = super().update(instance, validated_data)
        if tags:
            RecipeTag.objects.filter(recipe=instance).delete()
            for tag in tags:
                RecipeTag.objects.create(recipe=instance, tag=tag)
        if ingredients:
            IngredientAmountInRecipe.objects.filter(recipe=instance).delete()
            for data in ingredients:
                ingredient = get_object_or_404(Ingredient, id=data["id"])
                IngredientAmountInRecipe.objects.create(recipe=instance,
                                                        ingredient=ingredient,
                                                        amount=data["amount"])
        return instance


class MinifiedRecipeSerializer(ModelSerializer):
    """
    Serializes Recipe model instances with reduceed amount of fields.
    Only designed for displaying an already-existing model instance
    within the body of the response which replies to safe-methods request.
    """

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")
