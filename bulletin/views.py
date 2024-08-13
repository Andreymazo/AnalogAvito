from django.core.signing import BadSignature, Signer
from django.urls import reverse
from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    inline_serializer, extend_schema_view
)
from rest_framework import viewsets
from ad.models import Category
from bulletin.serializers import (
    CategorySerializer,

)


@extend_schema(
    tags=["Категории/Categories"],
)
@extend_schema_view(
    list=extend_schema(summary="Список всех категорий"),
    retrieve=extend_schema(summary="Получение информации о категории")
)
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для категорий."""
    http_method_names = ("get",)
    queryset = Category.objects.prefetch_related("children").all()
    serializer_class = CategorySerializer
