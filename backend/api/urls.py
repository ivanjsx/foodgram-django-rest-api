from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, RecipeViewSet, TagViewSet, UserViewSet

app_name: str = "api"


router_v1 = DefaultRouter()


router_v1.register(
    prefix="tags",
    viewset=TagViewSet,
    basename="tags",
)
router_v1.register(
    prefix="ingredients",
    viewset=IngredientViewSet,
    basename="ingredients",
)
router_v1.register(
    prefix="users",
    viewset=UserViewSet,
    basename="users",
)
router_v1.register(
    prefix="recipes",
    viewset=RecipeViewSet,
    basename="recipes",
)

handler404 = "api.utils.custom_404_handler"

urlpatterns = [
    path(
        route="auth/",
        view=include("djoser.urls.authtoken"),
        name="authtoken"
    ),
    path(
        route="",
        view=include(arg=router_v1.urls),
    ),
]
