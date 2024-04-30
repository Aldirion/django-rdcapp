"""
URL configuration for rdc_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# from sys import implementation
# from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
# from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.rdcapp_api import urls as api_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # path("api-auth/", include("rest_framework_simplejwt.authemtication"))
    # path("api-token-auth", TokenObtainPairView.as_view()),
    path("api/v1/", include(api_urls)),
]

if settings.DEBUG:
    from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
        path("api/schema", SpectacularAPIView.as_view(), name="schema"),
        path(
            "api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"
        ),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
