from django.urls import path
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Django Courses",
        default_version="v1",
        description="Django Courses API",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny, ),
)

urlpatterns = [
    path("api/v1/swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]
