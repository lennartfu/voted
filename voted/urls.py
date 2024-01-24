from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from voted import settings

urlpatterns = [
                  path("", include("product.urls")),
                  path('admin/', admin.site.urls),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
