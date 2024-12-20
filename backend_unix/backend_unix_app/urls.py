from django.urls import path
from .views import Command, RegisterView, Commandasync
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from rest_framework.permissions import AllowAny
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import LoginWithOTP, ValidateOTP

# Example DRF router (if you have viewsets)
router = DefaultRouter()

# Define your existing urlpatterns
urlpatterns = [
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=[AllowAny]),
        name="token_obtain_pair",
    ),
    path(
        "login/refresh/",
        TokenRefreshView.as_view(permission_classes=[AllowAny]),
        name="token_refresh",
    ),
    # Register endpoint is public
    path(
        "register/",
        RegisterView.as_view(permission_classes=[AllowAny]),
        name="sign_up",
    ),
    # Include DRF router for viewsets (ensure router urls are properly set up)
    # path("api/", include(router.urls)),
    # Documentation and schema view
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "login-with-otp/",
        LoginWithOTP.as_view(permission_classes=[AllowAny]),
        name="login-with-otp",
    ),
    path(
        "validate-otp/",
        ValidateOTP.as_view(permission_classes=[AllowAny]),
        name="validate-otp",
    ),
    path(
        "commands/",
        Command.as_view(permission_classes=[AllowAny]),
        name="commands",
    ),
    path(
        "commandsasync/",
        Commandasync.as_view(permission_classes=[AllowAny]),
        name="commandsasync",
    ),
]
