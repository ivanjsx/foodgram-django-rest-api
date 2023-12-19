import csv

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)

from recipes.models import Recipe
from users.models import CustomUser as User
from users.models import Subscription

from .serializers import (ChangePasswordSerializer, ExtendedUserShowSerializer,
                          MinifiedRecipeSerializer, QueryParamsSerializer)


def set_new_password(user, data):
    serializer = ChangePasswordSerializer(data=data,
                                          context={"user": user})
    serializer.is_valid(raise_exception=True)
    user.set_password(serializer.validated_data["new_password"])
    user.save()
    return Response(status=HTTP_204_NO_CONTENT)


def subscribe_to(pk, request):
    serializer = QueryParamsSerializer(data={"pk": pk})
    serializer.is_valid(raise_exception=True)
    if request.user.id == serializer.validated_data["pk"]:
        return Response(data={"error": "you cannot follow yourself"},
                        status=HTTP_400_BAD_REQUEST)
    subscription, _ = Subscription.objects.get_or_create(
        follower=request.user,
        influencer=get_object_or_404(User, id=serializer.validated_data["pk"])
    )
    output = ExtendedUserShowSerializer(
        instance=subscription.influencer,
        context={"request": request}
    )
    return Response(data=output.data, status=HTTP_201_CREATED)


def unsubscribe_from(pk, request):
    serializer = QueryParamsSerializer(data={"pk": pk})
    serializer.is_valid(raise_exception=True)
    influencer = get_object_or_404(User, id=serializer.validated_data["pk"])
    subscription = Subscription.objects.filter(follower=request.user.id,
                                               influencer=influencer.id)
    if subscription.exists():
        subscription.delete()
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


def reduce_cart(shopping_cart):
    output = {}
    for recipe in shopping_cart:
        for amount in recipe.ingredients.all():
            if amount.ingredient.id not in output.keys():
                output[amount.ingredient.id] = {
                    "measurement_unit": amount.ingredient.measurement_unit,
                    "name": amount.ingredient.name,
                    "amount": amount.amount,
                }
            else:
                output[amount.ingredient.id]["amount"] += amount.amount
    return output


def create_csv_response(shopping_cart):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        'attachment; filename="shopping_cart.csv"'
    )
    writer = csv.writer(response)
    writer.writerow(["Список продуктов"])
    for _, ingredient in shopping_cart.items():
        writer.writerow([ingredient["name"],
                         ingredient["amount"],
                         ingredient["measurement_unit"]])
    return response


def create_txt_response(shopping_cart):
    response = HttpResponse(content_type="text/plain")
    response["Content-Disposition"] = (
        'attachment; filename="shopping_cart.txt"'
    )
    response.write("Список продуктов\n")
    for _, ingredient in shopping_cart.items():
        response.write(f"{ingredient['name']}: "
                       f"{ingredient['amount']} "
                       f"{ingredient['measurement_unit']}\n")
    return response
