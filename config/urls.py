from config import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    # path("__debug__/", include("debug_toolbar.urls")),
]
urlpatterns += i18n_patterns(
    path("api/", include("bulletin.urls", namespace="bulletin")),
)

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path("__debug__/", include("debug_toolbar.urls")),)
# if not settings.TESTING:
#     urlpatterns = [
#         *urlpatterns,
#         path("__debug__/", include("debug_toolbar.urls")),
#     ]