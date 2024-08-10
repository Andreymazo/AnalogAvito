from django.core.signing import BadSignature, Signer
from django.urls import reverse
from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    inline_serializer
)
from rest_framework import viewsets
from ad.models import Category
from bulletin.serializers import (
    CategorySerializer,
   
)

from bulletin.utils import (
    check_ban,
    check_email_phone,
    create_or_update_code,
    get_tokens_for_user,
)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для категорий."""
    http_method_names = ("get",)
    queryset = Category.objects.prefetch_related("children").all()
    serializer_class = CategorySerializer
