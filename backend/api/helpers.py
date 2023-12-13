import csv

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)

from recipes.models import Recipe
from users.models import Subscription

from .serializers import (ChangePasswordSerializer, ExtendedUserShowSerializer,
                          MinifiedRecipeSerializer, QueryParamsSerializer)

User = get_user_model()


def set_new_password(user, data):
    serializer = ChangePasswordSerializer(data=data,
                                          context={"user": user})
    serializer.is_valid(raise_exception=True)
    user.set_password(serializer.validated_data["new_password"])
    user.save()
    return Response(status=HTTP_204_NO_CONTENT)

def add_recipe_to_user_list(list_model, user, pk):
    serializer = QueryParamsSerializer(data={"pk": pk})
    serializer.is_valid(raise_exception=True)
    recipe = get_object_or_404(Recipe, id=serializer.validated_data["pk"])
    item, _ = list_model.objects.get_or_create(user=user,
                                               recipe=recipe)
    output = MinifiedRecipeSerializer(instance=item.recipe)
    return Response(data=output.data, status=HTTP_201_CREATED)


def remove_recipe_from_user_list(list_model, user, pk):
    serializer = QueryParamsSerializer(data={"pk": pk})
    serializer.is_valid(raise_exception=True)
    recipe = get_object_or_404(Recipe, id=serializer.validated_data["pk"])
    item = list_model.objects.filter(user=user.id,
                                     recipe=recipe.id)
    if item.exists():
        item.delete()
    return Response(status=HTTP_204_NO_CONTENT)

