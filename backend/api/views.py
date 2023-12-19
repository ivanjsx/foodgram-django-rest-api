from http import HTTPMethod

from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404

from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from recipes.models import CartItem, FavoriteItem, Ingredient, Recipe, Tag
from users.models import CustomUser as User

from .filters import (FilterIngredientsByName, FilterRecipesByTagsAndAuthor,
                      filter_recipes_by_query_params)
from .helpers import (add_recipe_to_user_list, create_csv_response,
                      create_txt_response, reduce_cart,
                      remove_recipe_from_user_list, set_new_password,
                      subscribe_to, unsubscribe_from)
from .mixins import ListCreateRetrieveMixin, PartialUpdateOnlyMixin
from .paginators import CustomPageSizePagination
from .permissions import (IsAdminOrReadOnly, RecipeViewSetPermission,
                          SetOnesPasswordActionPermission,
                          UserViewSetPermission)
from .serializers import (DefaultRecipeSerializer, ExtendedUserShowSerializer,
                          IngredientSerializer, QueryParamsSerializer,
                          TagSerializer, UserCreateSerializer,
                          UserShowSerializer)


class TagViewSet(ModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly, )


class IngredientViewSet(ModelViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly, )
    filterset_class = FilterIngredientsByName


class UserViewSet(GenericViewSet, ListCreateRetrieveMixin):

    queryset = User.objects.all()
    permission_classes = (UserViewSetPermission, )
    pagination_class = CustomPageSizePagination

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return UserShowSerializer
        return UserCreateSerializer

    def perform_create(self, serializer):
        serializer.save(
            password=make_password(serializer.validated_data["password"])
        )

    @action(detail=False,
            methods=(HTTPMethod.GET, ),
            permission_classes=(IsAuthenticated, ))
    def me(self, request):
        serializer = self.get_serializer(instance=request.user)
        return Response(data=serializer.data, status=HTTP_200_OK)

    @action(detail=False,
            methods=(HTTPMethod.POST, ),
            url_path="set_password",
            permission_classes=(IsAuthenticated, ))
    def set_own_password(self, request):
        return set_new_password(request.user, request.data)

    @action(detail=True,
            methods=(HTTPMethod.POST, ),
            url_path="set_password",
            permission_classes=(SetOnesPasswordActionPermission, ))
    def set_ones_password(self, request, pk=None):
        serializer = QueryParamsSerializer(data={"pk": pk})
        serializer.is_valid(raise_exception=True)
        return set_new_password(
            get_object_or_404(User, id=serializer.validated_data["pk"]),
            request.data
        )

    @action(detail=True,
            permission_classes=(IsAuthenticated, ),
            methods=(HTTPMethod.POST, HTTPMethod.DELETE))
    def subscribe(self, request, pk=None):
        if request.method == HTTPMethod.POST:
            return subscribe_to(pk, request)
        return unsubscribe_from(pk, request)

    @action(detail=False,
            methods=(HTTPMethod.GET, ),
            permission_classes=(IsAuthenticated, ))
    def subscriptions(self, request):
        queryset = self.get_queryset().filter(followers__follower=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ExtendedUserShowSerializer(
                instance=page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)
        serializer = ExtendedUserShowSerializer(
            instance=queryset, many=True, context={"request": request}
        )
        return Response(data=serializer.data, status=HTTP_200_OK)


class RecipeViewSet(ModelViewSet, PartialUpdateOnlyMixin):

    serializer_class = DefaultRecipeSerializer
    permission_classes = (RecipeViewSetPermission, )
    pagination_class = CustomPageSizePagination
    filterset_class = FilterRecipesByTagsAndAuthor

    def get_queryset(self):
        user = self.request.user
        queryset = Recipe.objects.all()
        params = self.request.query_params

        data = {}
        if params.get("is_favorited", None):
            data["is_favorited"] = params["is_favorited"]
        if params.get("is_in_shopping_cart", None):
            data["is_in_shopping_cart"] = params["is_in_shopping_cart"]

        serializer = QueryParamsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return filter_recipes_by_query_params(
            queryset, user, serializer.validated_data
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True,
            permission_classes=(IsAuthenticated, ),
            methods=(HTTPMethod.POST, HTTPMethod.DELETE))
    def favorite(self, request, pk=None):
        if request.method == HTTPMethod.POST:
            return add_recipe_to_user_list(FavoriteItem, request.user, pk)
        return remove_recipe_from_user_list(FavoriteItem, request.user, pk)

    @action(detail=True,
            permission_classes=(IsAuthenticated, ),
            methods=(HTTPMethod.POST, HTTPMethod.DELETE))
    def shopping_cart(self, request, pk=None):
        if request.method == HTTPMethod.POST:
            return add_recipe_to_user_list(CartItem, request.user, pk)
        return remove_recipe_from_user_list(CartItem, request.user, pk)

    @action(detail=False,
            methods=(HTTPMethod.GET, ),
            permission_classes=(IsAuthenticated, ))
    def download_shopping_cart(self, request):
        queryset = Recipe.objects.filter(
            carts_in__user=request.user.id
        ).prefetch_related("ingredients").all()
        cart = reduce_cart(queryset)
        fileformat = request.query_params.get("fileformat", "txt")
        if fileformat == "csv":
            return create_csv_response(cart)
        return create_txt_response(cart)
