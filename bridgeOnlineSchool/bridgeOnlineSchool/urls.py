from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from . import settings


urlpatterns = [
    path("", include("landing.urls")),
    path("authentication/", include("authentication.urls")),
    path("cart/", include("shoppingCard.urls")),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)