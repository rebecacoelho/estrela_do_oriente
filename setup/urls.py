"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from creche.views.aluno import AlunoViewSet
from creche.views.documento import DocumentoViewSet
# from creche.views.diretor import DiretorViewSet  # REMOVIDO - Não é mais necessário
from creche.views.responsavel import ResponsavelViewSet
from creche.views.user import RegisterView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Schema view para drf_yasg (compatibilidade)
schema_view = get_schema_view(
    openapi.Info(
        title="Estrela do Oriente API",
        default_version='v1',
        description="API para gerenciamento da creche Estrela do Oriente",
    ),
    public=True,
    permission_classes=[AllowAny],
)

router = routers.DefaultRouter()
router.register(r"alunos", AlunoViewSet)
router.register(r"documentos", DocumentoViewSet)
router.register(r"responsaveis", ResponsavelViewSet)
# router.register(r"diretores", DiretorViewSet)  # REMOVIDO - Não é mais necessário
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/register/", RegisterView.as_view(), name="register"),
    path("api/", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('api/schema/',SpectacularAPIView.as_view(),name='schema'),
    path(
        'api/schema/swagger-ui/',
        SpectacularSwaggerView.as_view(
            permission_classes=[AllowAny], url_name='schema'
        ),
        name='swagger-ui',
    ),
    path(
        'api/schema/redoc/',
        SpectacularRedocView.as_view(
            permission_classes=[AllowAny], url_name='schema'
        ),
        name='redoc',
    ),
    # URLs antigas do drf_yasg para compatibilidade
    path("api/swagger.json/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path(
        "api/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
