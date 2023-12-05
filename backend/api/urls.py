from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, TagViewSet

app_name: str = "api"


router_v1 = DefaultRouter()

router_v1.register(
    prefix="tags", viewset=TagViewSet, basename="tags",
)
router_v1.register(
    prefix="ingredients", viewset=IngredientViewSet, basename="ingredients",
)

urlpatterns = [
    path(
        route="v1/",
        view=include(arg=router_v1.urls),
    ),
]
